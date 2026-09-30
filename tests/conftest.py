import uuid

import pytest

from api_clients.user_api import UserAPI
from api_clients.product_api import ProductAPI
from api_clients.order_api import OrderAPI
from config.settings import BASE_URL
pytest_plugins = ["utils.test_result_reporter"]


@pytest.fixture
def user_api():
    return UserAPI(BASE_URL)


@pytest.fixture
def product_api():
    return ProductAPI(BASE_URL)


@pytest.fixture
def order_api():
    return OrderAPI(BASE_URL)


@pytest.fixture
def test_user(user_api):
    unique_id = uuid.uuid4().hex[:8]

    payload = {
        "username": f"fixture_user_{unique_id}",
        "email": f"fixture_{unique_id}@example.com",
        "password": "Test@123",
    }

    response = user_api.create_user(payload)

    assert response.status_code == 201

    data = response.json()

    return {
        "id": data["id"],
        "username": payload["username"],
        "email": payload["email"],
        "password": payload["password"],
    }


@pytest.fixture
def test_product(product_api):
    unique_id = uuid.uuid4().hex[:8]

    payload = {
        "name": f"Fixture_Product_{unique_id}",
        "description": "Product created by pytest fixture",
        "price": 2500,
        "category": "Testing",
    }

    response = product_api.create_product(payload)

    assert response.status_code == 201

    data = response.json()

    return {
        "id": data["id"],
        "name": payload["name"],
        "description": payload["description"],
        "price": payload["price"],
        "category": payload["category"],

    }

@pytest.fixture
def browser_context_args(browser_context_args):
    return {
        **browser_context_args,
        "record_video_dir": "test-results/videos",
    }

@pytest.fixture
def browser_context_args(browser_context_args):
    return {
        **browser_context_args,
        "record_video_dir": "test-results/videos",
    }