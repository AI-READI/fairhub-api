"""Utils for core"""

import requests


def request_json(url):
    """ "Request JSON from URL"""
    try:
        response = requests.request("GET", url, headers={}, data={}, timeout=10)

        return response.json()
    except Exception as e:
        raise e
