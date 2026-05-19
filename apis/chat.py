from flask_restx import Namespace, Resource
from flask import request, jsonify
from dotenv import load_dotenv

from openai import AzureOpenAI

import os

import time
from collections import defaultdict, deque
from threading import Lock

requests_log: defaultdict[str, deque[float]] = defaultdict(deque)
rate_lock = Lock()


def is_rate_limited(ip, limit=15, window=60):
    now = time.time()
    with rate_lock:
        q = requests_log[ip]
        while q and q[0] < now - window:
            q.popleft()
        if len(q) >= limit:
            return True
        q.append(now)
        return False


# Key auth
endpoint = os.getenv("ENDPOINT_URL")
deployment = os.getenv("DEPLOYMENT_NAME")
search_endpoint = os.getenv("SEARCH_ENDPOINT")
search_key = os.getenv("SEARCH_KEY")
search_index = os.getenv("SEARCH_INDEX_NAME")
subscription_key = os.getenv("AZURE_OPENAI_API_KEY")
index_name = os.getenv("INDEX_NAME")

# Key auth Initialize Azure OpenAI client
client = AzureOpenAI(
    azure_endpoint=endpoint,
    api_key=subscription_key,
    api_version="2025-01-01-preview",
)


api = Namespace("Chat", description="Aireadi chatbox", path="/")

load_dotenv()


@api.route("/chat")
class ChatBox(Resource):
    @api.response(201, "Success")
    @api.response(400, "Validation Error")
    def post(self):
        ip = request.remote_addr
        if is_rate_limited(ip):
            return jsonify({"error": "Too many requests"}), 429

        data = request.get_json(silent=True)
        if not data or not isinstance(data, dict):
            return jsonify({"error": "Body must be JSON"}), 400
        question = data.get("question")
        if not question or not isinstance(question, str) or not question.strip():
            return jsonify({"error": "'question' is required"}), 400
        question = question.strip()
        if len(question) > 1200:
            return jsonify({"error": "'question' too long"}), 400

        prompt = """You are answering questions about the AI-READI dataset using documentation.
                    Read the context carefully and answer the question. When you find something,
                     only answer the direct answer, do not say "According to the documentation,"
                    If you are not confident the context contains the correct answer,
                     say: "Not found in the provided pages"."""

        messages = [
            {
                "role": "system",
                "content": prompt,
            },
            {
                "role": "user",
                "content": question,
            }
        ]
        try:
            completion = client.chat.completions.create(
                model=deployment,
                messages=messages,
                max_tokens=450,
                temperature=0.3,
                top_p=1.0,
                frequency_penalty=0,
                presence_penalty=0,
                stop=None,
                stream=False,
                extra_body={
                    "data_sources": [{
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
                            "authentication": {
                                "type": "api_key",
                                "key": f"{search_key}"
                            }
                        }
                    }]
                }
            )
            answer = completion.choices[0].message.content

        except Exception as e:
            print("Completion failed")
            msg = str(e).lower()
            if "rate limit" in msg or "429" in msg:
                return jsonify({"error": "Service busy"}), 429

            return jsonify({"error": "Internal server error"}), 500

        return jsonify({"answer": answer})
