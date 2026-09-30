import requests


class UserAPI:
    def __init__(self, base_url: str):
        self.base_url = base_url

    def create_user(self, payload: dict):
        return requests.post(
            f"{self.base_url}/users/",
            json=payload,
        )

    def get_user(self, user_id: int):
        return requests.get(
            f"{self.base_url}/users/{user_id}"
        )