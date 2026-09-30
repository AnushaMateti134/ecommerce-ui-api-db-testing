import uuid
def test_create_order_with_zero_quantity(
    user_api,
    product_api,
    order_api,
):
    unique_id = uuid.uuid4().hex[:8]

    user_response = user_api.create_user(
    {
        "username": f"validation_user_{unique_id}",
        "email": f"validation_{unique_id}@example.com",
        "password": "Test@123",
    }
)

    assert user_response.status_code == 201

    user_id = user_response.json()["id"]

    product_response = product_api.create_product(
        {
            "name": "Validation Product",
            "description": "Product for validation testing",
            "price": 1000,
            "category": "Testing",
        }
    )

    assert product_response.status_code == 201

    product_id = product_response.json()["id"]

    response = order_api.create_order(
        {
            "user_id": user_id,
            "items": [
                {
                    "product_id": product_id,
                    "quantity": 0,
                }
            ],
        }
    )

    assert response.status_code == 422
def test_create_order_with_empty_items(
    user_api,
    order_api,
):
    unique_id = uuid.uuid4().hex[:8]

    user_response = user_api.create_user(
        {
            "username": f"empty_order_user_{unique_id}",
            "email": f"empty_order_{unique_id}@example.com",
            "password": "Test@123",
        }
    )

    assert user_response.status_code == 201

    user_id = user_response.json()["id"]

    response = order_api.create_order(
        {
            "user_id": user_id,
            "items": [],
        }
    )

    assert response.status_code == 422

def test_create_order_with_negative_quantity(
    user_api,
    product_api,
    order_api,
):
    unique_id = uuid.uuid4().hex[:8]

    # Create user
    user_response = user_api.create_user(
        {
            "username": f"negative_qty_user_{unique_id}",
            "email": f"negative_qty_{unique_id}@example.com",
            "password": "Test@123",
        }
    )

    assert user_response.status_code == 201

    user_id = user_response.json()["id"]

    # Create product
    product_response = product_api.create_product(
        {
            "name": f"Negative_Quantity_Product_{unique_id}",
            "description": "Product for negative quantity testing",
            "price": 1000,
            "category": "Testing",
        }
    )

    assert product_response.status_code == 201

    product_id = product_response.json()["id"]

    # Attempt order with negative quantity
    response = order_api.create_order(
        {
            "user_id": user_id,
            "items": [
                {
                    "product_id": product_id,
                    "quantity": -1,
                }
            ],
        }
    )

    assert response.status_code == 422