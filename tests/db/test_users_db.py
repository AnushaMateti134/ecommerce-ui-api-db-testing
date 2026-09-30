import uuid

from db.db_helper import get_user_by_id


def test_created_user_exists_in_database(user_api):
    unique_id = uuid.uuid4().hex[:8]

    payload = {
        "username": f"db_test_user_{unique_id}",
        "email": f"db_test_{unique_id}@example.com",
        "password": "Test@123",
    }

    response = user_api.create_user(payload)

    assert response.status_code == 201

    user_id = response.json()["id"]

    db_user = get_user_by_id(user_id)

    assert db_user is not None
    assert db_user["id"] == user_id
    assert db_user["username"] == payload["username"]
    assert db_user["email"] == payload["email"]