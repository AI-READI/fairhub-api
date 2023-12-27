"""Utils for core"""
import requests


def request_json(url):
    """ "Request JSON from URL"""
    try:
        payload = {}
        headers = {}

        response = requests.request(
            "GET", url, headers=headers, data=payload, timeout=10
        )

        return response.json()
    except Exception as e:
        raise e
