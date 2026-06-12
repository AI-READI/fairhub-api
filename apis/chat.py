"""Chat API endpoint."""

import re
import time
from collections import defaultdict, deque
from threading import Lock
from typing import Any

from dotenv import load_dotenv
from flask import Response, request, stream_with_context
from flask_restx import Namespace, Resource
from openai import AzureOpenAI

import config

load_dotenv()

requests_log: defaultdict[str, deque[float]] = defaultdict(deque)
rate_lock = Lock()


def is_rate_limited(ip_address, limit=15, window=60):
    """rate limit"""
    now = time.time()
    with rate_lock:
        query = requests_log[ip_address]
        while query and query[0] < now - window:
            query.popleft()
        if len(query) >= limit:
            return True
        query.append(now)
        return False


api = Namespace("Chat", description="Aireadi chatbox", path="/")

# Key auth
endpoint = config.ENDPOINT_URL
DEPLOYMENT = "gpt-4o-mini"
search_endpoint = config.SEARCH_ENDPOINT
search_key = config.SEARCH_KEY
search_index = config.SEARCH_INDEX_NAME
subscription_key = config.AZURE_OPENAI_API_KEY
index_name = config.INDEX_NAME

# Key auth Initialize Azure OpenAI client
client = AzureOpenAI(
    azure_endpoint=endpoint,
    api_key=subscription_key,
    api_version="2025-01-01-preview",
)

BLOCKED_PATTERNS = [
    ("ignore", "previous"),
    ("ignore", "prior"),
    ("ignore", "above"),
    ("forget", "instruction"),
    ("forget", "you are"),
    ("forget", "your role"),
    ("disregard", "previous"),
    ("disregard", "instruction"),
    ("reveal", "prompt"),
    ("reveal", "instruction"),
    ("show me your", "prompt"),
    ("show me your", "instruction"),
]

BLOCKED_PHRASES = [
    "system prompt",
    "jailbreak",
    "dan mode",
    "developer mode",
    "pretend you are",
    "act as a",
    "you are now",
]


@api.route("/chat")
class ChatBox(Resource):
    """chat endpoint"""

    @api.response(200, "Success")
    @api.response(400, "Validation Error")
    def post(self):  # pylint: disable=too-many-return-statements
        """Process chat request and return AI response."""
        ip_address = request.remote_addr
        if is_rate_limited(ip_address):
            return {"error": "Too many requests"}, 429

        data = request.get_json(silent=True)
        if not data or not isinstance(data, dict):
            return {"error": "Body must be JSON"}, 400

        question = data.get("question")

        if not question or not isinstance(question, str) or not question.strip():
            return {"error": "'question' is required"}, 400

        question = question.strip()
        if len(question) > 1200:
            return {"error": "'question' too long"}, 400

        q = question.lower()

        # Check for two-word injection patterns
        for word1, word2 in BLOCKED_PATTERNS:
            if word1 in q and word2 in q:
                return Response(
                    "I can only help with AI-READI dataset-related questions.",
                    mimetype="text/plain",
                )
        # Check for single blocked phrases
        for phrase in BLOCKED_PHRASES:
            if phrase in q:
                return Response(
                    "I can only help with AI-READI dataset-related questions.",
                    mimetype="text/plain",
                )

        prompt = (
            "You are answering questions about the AI-READI dataset using documentation."
            "Read the context carefully and answer the question. When you find something,"
            "only answer the direct answer, do not say 'According to the documentation',"
            "If you are not confident the context contains the correct answer,"
            "say: 'Not found in the provided pages'."
        )

        messages = [
            {"role": "system", "content": prompt},
            {"role": "user", "content": question},
        ]

        extra_body: dict[str, Any] = {
            "data_sources": [
                {
                    "type": "azure_search",
                    "parameters": {
                        "endpoint": f"{search_endpoint}",
                        "index_name": f"{index_name}",
                        "semantic_configuration": "default",
                        "query_type": "semantic",
                        "fields_mapping": {},
                        "in_scope": True,
                        "filter": None,
                        "strictness": 3,
                        "top_n_documents": 5,
                        "authentication": {"type": "api_key", "key": f"{search_key}"},
                    },
                }
            ]
        }

        def generate():
            streaming = None
            try:

                streaming = client.chat.completions.create(
                    model=DEPLOYMENT,
                    messages=messages,  # type: ignore[arg-type]
                    max_tokens=450,
                    temperature=0.3,
                    top_p=1.0,
                    stream=True,
                    frequency_penalty=0,
                    presence_penalty=0,
                    stop=None,
                    extra_body=extra_body,
                )
                # assert isinstance(streaming, ChatCompletion)

                buffer = ""
                for chunk in streaming:   # pylint: disable=not-an-iterable
                    if not (chunk.choices and chunk.choices[0].delta.content):  # type: ignore[union-attr]
                        continue
                    buffer += chunk.choices[0].delta.content  # type: ignore[union-attr]
                    cut = buffer.rfind("[")
                    if cut == -1:
                        yield re.sub(r"\s*\[doc\d*\]", "", buffer)
                        buffer = ""
                    else:
                        yield re.sub(r"\s*\[doc\d*\]", "", buffer[:cut])
                        buffer = buffer[cut:]
                if buffer:
                    yield re.sub(r"\s*\[doc\d*\]", "", buffer)

            except GeneratorExit:
                if streaming is not None:
                    streaming.close()  # type: ignore[union-attr]
                raise
            except Exception as error:  # pylint: disable=broad-exception-caught
                print("Completion failed...")
                msg = str(error).lower()
                if "content_filter" in msg or "content filter" in msg:
                    yield "I can only help with AI-READI dataset-related questions."
                elif "rate limit" in msg or "429" in msg:
                    yield "Service busy, please try again"
                else:
                    yield "Sorry, something went wrong."

        return Response(stream_with_context(generate()), mimetype="text/plain")


@api.route("/health")
class Health(Resource):
    def get(self):
        return {"status": "ok"}, 200