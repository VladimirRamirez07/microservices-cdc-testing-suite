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

    def list_orders(self, status: str = None) -> list:
        params = {"status": status} if status else {}
        response = requests.get(f"{self.base_url}/orders", params=params)
        if response.status_code == 400:
            return {"error": response.json().get("error")}
        response.raise_for_status()
        return response.json()

    def create_order(self, product: str, quantity: int) -> dict:
        payload = {"product": product, "quantity": quantity}
        response = requests.post(f"{self.base_url}/orders", json=payload)
        if response.status_code in (400, 422):
            return {"error": response.json().get("error")}
        response.raise_for_status()
        return response.json()

    def update_status(self, order_id: int, status: str) -> dict:
        payload = {"status": status}
        response = requests.patch(f"{self.base_url}/orders/{order_id}/status", json=payload)
        if response.status_code == 404:
            return None
        if response.status_code == 400:
            return {"error": response.json().get("error")}
        response.raise_for_status()
        return response.json()

    def delete_order(self, order_id: int) -> dict:
        response = requests.delete(f"{self.base_url}/orders/{order_id}")
        if response.status_code == 404:
            return None
        response.raise_for_status()
        return response.json()

    def get_health(self) -> dict:
        response = requests.get(f"{self.base_url}/health")
        response.raise_for_status()
        return response.json()