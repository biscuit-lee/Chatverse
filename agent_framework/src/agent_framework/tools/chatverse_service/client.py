import os
import requests


class ChatverseClient:
    def __init__(self, api_key: str = None, base_url: str = None):
        self.base_url = base_url or os.getenv("CHATVERSE_BASE_URL", "http://localhost:8080")
        self.api_key = api_key or os.getenv("CHATVERSE_API_KEY")

    def _headers(self):
        return {"X-API-KEY": self.api_key}

    def get(self, path: str, params: dict = None):
        url = f"{self.base_url}/{path.lstrip('/')}"
        response = requests.get(url, headers=self._headers(), params=params)
        response.raise_for_status()
        return response.json()

    def post(self, path: str, json: dict = None):
        url = f"{self.base_url}/{path.lstrip('/')}"
        response = requests.post(url, headers=self._headers(), json=json)
        response.raise_for_status()
        return response.json()
