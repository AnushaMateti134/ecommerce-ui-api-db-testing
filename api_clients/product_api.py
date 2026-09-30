import requests


class ProductAPI:
    def __init__(self, base_url: str):
        self.base_url = base_url

    def create_product(self, payload: dict):
        return requests.post(
            f"{self.base_url}/products/",
            json=payload,
        )

    def get_product(self, product_id: int):
        return requests.get(
            f"{self.base_url}/products/{product_id}"
        )