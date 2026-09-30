import requests


class OrderAPI:
    def __init__(self, base_url: str):
        self.base_url = base_url

    def create_order(self, payload: dict):
        return requests.post(
            f"{self.base_url}/orders/",
            json=payload,
        )

    def get_order(self, order_id: int):
        return requests.get(
            f"{self.base_url}/orders/{order_id}"
        )