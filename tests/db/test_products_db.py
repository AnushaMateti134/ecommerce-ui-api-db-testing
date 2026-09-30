import uuid

from db.db_helper import get_product_by_id


def test_created_product_exists_in_database(product_api):
    unique_id = uuid.uuid4().hex[:8]

    payload = {
        "name": f"DB_Test_Product_{unique_id}",
        "description": "Database validation product",
        "price": 2500,
        "category": "Testing",
    }

    response = product_api.create_product(payload)

    assert response.status_code == 201

    product_id = response.json()["id"]

    db_product = get_product_by_id(product_id)

    assert db_product is not None
    assert db_product["id"] == product_id
    assert db_product["name"] == payload["name"]
    assert db_product["description"] == payload["description"]
    assert db_product["price"] == payload["price"]
    assert db_product["category"] == payload["category"]