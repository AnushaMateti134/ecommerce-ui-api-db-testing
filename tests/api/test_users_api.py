

import uuid

from db.db_helper import get_user_by_id
from api_clients.user_api import UserAPI
from config.settings import BASE_URL


user_api = UserAPI(BASE_URL)

def test_create_user(user_api):
    unique_id = uuid.uuid4().hex[:8]

    payload = {
        "username": f"testuser_{unique_id}",
        "email": f"test_{unique_id}@example.com",
        "password": "Test@123",
    }

    response = user_api.create_user(payload)

    assert response.status_code == 201

    data = response.json()

    assert data["id"] > 0
    assert data["username"] == payload["username"]
    assert data["email"] == payload["email"]
    assert "password" not in data

    user_id = data["id"]

    db_user = get_user_by_id(user_id)

    assert db_user is not None
    assert db_user["id"] == user_id
    assert db_user["username"] == payload["username"]
    assert db_user["email"] == payload["email"]

def test_get_nonexistent_user():
    response = user_api.get_user(999999)

    

    assert response.status_code == 404
    assert response.json()["detail"] == "User not found"
def test_create_user_with_invalid_email():
    unique_id = uuid.uuid4().hex[:8]

    payload = {
        "username": f"invalid_email_{unique_id}",
        "email": "not-an-email",
        "password": "Test@123",
    }

    response = user_api.create_user(payload)
    

    assert response.status_code == 422
def test_create_user_missing_username():
    unique_id = uuid.uuid4().hex[:8]

    payload = {
        "email": f"missing_{unique_id}@example.com",
        "password": "Test@123",
    }

    response = user_api.create_user(payload)
    

    assert response.status_code == 422
    import uuid

import requests


def test_create_user():
    unique_id = uuid.uuid4().hex[:8]

    payload = {
        "username": f"testuser_{unique_id}",
        "email": f"test_{unique_id}@example.com",
        "password": "Test@123",
    }

    response = requests.post(
        f"{BASE_URL}/users/",
        json=payload,
    )

    assert response.status_code == 201

    data = response.json()

    assert data["id"] > 0
    assert data["username"] == payload["username"]
    assert data["email"] == payload["email"]
    assert "password" not in data


def test_create_user_with_duplicate_username(user_api):
    unique_id = uuid.uuid4().hex[:8]

    payload = {
        "username": f"duplicate_{unique_id}",
        "email": f"duplicate_{unique_id}@example.com",
        "password": "Test@123",
    }

    first_response = user_api.create_user(payload)

    assert first_response.status_code == 201

    duplicate_response = user_api.create_user(
        {
            "username": payload["username"],
            "email": f"another_{unique_id}@example.com",
            "password": "Test@456",
        }
    )

    assert duplicate_response.status_code == 409
    assert duplicate_response.json()["detail"] == "Username already exists"


def test_get_nonexistent_user(user_api):
    response = user_api.get_user(999999)

    assert response.status_code == 404
    assert response.json()["detail"] == "User not found"


def test_create_user_with_invalid_email(user_api):
    unique_id = uuid.uuid4().hex[:8]

    payload = {
        "username": f"invalid_email_{unique_id}",
        "email": "not-an-email",
        "password": "Test@123",
    }

    response = user_api.create_user(payload)

    assert response.status_code == 422
def test_create_user_missing_username(user_api):
    unique_id = uuid.uuid4().hex[:8]

    payload = {
        "email": f"missing_{unique_id}@example.com",
        "password": "Test@123",
    }

    response = user_api.create_user(payload)

    assert response.status_code == 422