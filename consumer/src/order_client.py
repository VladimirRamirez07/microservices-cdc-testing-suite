import requests

class OrderClient:
    def __init__(self, base_url: str):
        self.base_url = base_url

    def get_order(self, order_id: int) -> dict:
        response = requests.get(f"{self.base_url}/orders/{order_id}")
        if response.status_code == 404:
            return None
        response.raise_for_status()
        return response.json()

    def get_health(self) -> dict:
        response = requests.get(f"{self.base_url}/health")
        response.raise_for_status()
        return response.json()