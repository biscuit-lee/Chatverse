import os
import requests

class ChatverseClient:
    def __init__(self):
        self.base_url = os.getenv("CHATVERSE_BASE_URL", "http://localhost:8000")
        self.api_key = os.getenv("CHATVERSE_API_KEY", "default_api_key")

    def _headers(self):
        return {"Authorization": f"Bearer {self.api_key}"}
    
    def get(self, path: str, params: dict = None):
        url = f"{self.base_url}/{path.lstrip('/')}"
        response = requests.get(url, headers=self._headers(), params=params)
        response.raise_for_status()
        return response.json()
    
    def post(self, path: str, load: dict = None):
        response = requests.post(f"{self.base_url}/{path}", json=load)
        response.raise_for_status()
        return response.json()
    
client = ChatverseClient()