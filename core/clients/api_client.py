import requests
from core.config.settings import Settings


class APIClient:
    def __init__(self):
        self.base_url = Settings.get_base_url()
        self.session = requests.Session()

    def request(self, method, endpoint, **kwargs):
        url = f"{self.base_url}{endpoint}"
        return self.session.request(method, url, **kwargs)

    def get(self, endpoint, params=None):
        return self.request("GET", endpoint, params=params)

    def post(self, endpoint, data=None):
        return self.request("POST", endpoint, json=data)

    def put(self, endpoint, data=None):
        return self.request("PUT", endpoint, json=data)

    def delete(self, endpoint):
        return self.request("DELETE", endpoint)