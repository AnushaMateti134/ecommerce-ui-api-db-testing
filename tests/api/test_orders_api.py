import uuid


def create_test_user(user_api):
    unique_id = uuid.uuid4().hex[:8]

    payload = {
        "username": f"order_user_{unique_id}",
        "email": f"order_{unique_id}@example.com",
        "password": "Test@123",
    }

    response = user_api.create_user(payload)

    assert response.status_code == 201

    return response.json()["id"]


def create_test_product(product_api):
    unique_id = uuid.uuid4().hex[:8]

    payload = {
        "name": f"Order_Product_{unique_id}",
        "description": "Product for order testing",
        "price": 2500,
        "category": "Testing",
    }

    response = product_api.create_product(payload)

    assert response.status_code == 201

    return response.json()["id"], payload["price"]


def test_create_order(user_api, product_api, order_api):
    user_id = create_test_user(user_api)
    product_id, product_price = create_test_product(product_api)

    payload = {
        "user_id": user_id,
        "items": [
            {
                "product_id": product_id,
                "quantity": 2,
            }
        ],
    }

    response = order_api.create_order(payload)

    assert response.status_code == 201

    data = response.json()

    assert data["id"] > 0
    assert data["user_id"] == user_id
    assert data["total_amount"] == product_price * 2
    assert data["status"] == "created"


def test_get_existing_order(user_api, product_api, order_api):
    user_id = create_test_user(user_api)
    product_id, product_price = create_test_product(product_api)
    payload = {
        "user_id": user_id,
        "items": [
            {
                "product_id": product_id,
                "quantity": 1,
            }
        ],
    }

    create_response = order_api.create_order(payload)

    assert create_response.status_code == 201

    order_id = create_response.json()["id"]

    response = order_api.get_order(order_id)

    assert response.status_code == 200

    data = response.json()

    assert data["id"] == order_id
    assert data["user_id"] == user_id
    assert data["total_amount"] == product_price
    assert data["status"] == "created"


def test_get_nonexistent_order(order_api):
    response = order_api.get_order(999999)

    assert response.status_code == 404
    assert response.json()["detail"] == "Order not found"


def test_create_order_with_invalid_user(product_api, order_api):
    product_id, _ = create_test_product(product_api)

    payload = {
        "user_id": 999999,
        "items": [
            {
                "product_id": product_id,
                "quantity": 1,
            }
        ],
    }

    response = order_api.create_order(payload)

    assert response.status_code == 404
    assert response.json()["detail"] == "User not found"


def test_create_order_with_invalid_product(user_api, order_api):
    user_id = create_test_user(user_api)

    payload = {
        "user_id": user_id,
        "items": [
            {
                "product_id": 999999,
                "quantity": 1,
            }
        ],
    }

    response = order_api.create_order(payload)

    assert response.status_code == 404
    assert response.json()["detail"] == "Product 999999 not found"