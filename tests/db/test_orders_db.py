import uuid

from db.db_helper import (
    get_order_by_id,
    get_order_items_by_order_id,
)


def test_created_order_exists_in_database(
    user_api,
    product_api,
    order_api,
):
    unique_id = uuid.uuid4().hex[:8]

    # Create test user
    user_response = user_api.create_user(
        {
            "username": f"db_order_user_{unique_id}",
            "email": f"db_order_{unique_id}@example.com",
            "password": "Test@123",
        }
    )

    assert user_response.status_code == 201

    user_id = user_response.json()["id"]

    # Create test product
    product_response = product_api.create_product(
        {
            "name": f"DB_Order_Product_{unique_id}",
            "description": "Product for DB order testing",
            "price": 3000,
            "category": "Testing",
        }
    )

    assert product_response.status_code == 201

    product_id = product_response.json()["id"]

    # Create order
    order_response = order_api.create_order(
        {
            "user_id": user_id,
            "items": [
                {
                    "product_id": product_id,
                    "quantity": 2,
                }
            ],
        }
    )

    assert order_response.status_code == 201

    order_id = order_response.json()["id"]

    # Validate order table
    db_order = get_order_by_id(order_id)

    assert db_order is not None
    assert db_order["id"] == order_id
    assert db_order["user_id"] == user_id
    assert db_order["total_amount"] == 6000
    assert db_order["status"] == "created"

    # Validate order_items table
    db_items = get_order_items_by_order_id(order_id)

    assert len(db_items) == 1

    db_item = db_items[0]

    assert db_item["order_id"] == order_id
    assert db_item["product_id"] == product_id
    assert db_item["quantity"] == 2
    assert db_item["price"] == 3000