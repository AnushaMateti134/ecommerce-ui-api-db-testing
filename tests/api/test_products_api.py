import uuid

from db.db_helper import get_product_by_id





def test_create_product(product_api):
    unique_id = uuid.uuid4().hex[:8]

    payload = {
        "name": f"Laptop_{unique_id}",
        "description": "QA Test Laptop",
        "price": 75000,
        "category": "Electronics",
    }

    response = product_api.create_product(payload)
    

    assert response.status_code == 201

    data = response.json()

    assert data["id"] > 0
    assert data["name"] == payload["name"]
    assert data["description"] == payload["description"]
    assert data["price"] == payload["price"]
    assert data["category"] == payload["category"]

    product_id = data["id"]

    db_product = get_product_by_id(product_id)

    assert db_product is not None
    assert db_product["id"] == product_id
    assert db_product["name"] == payload["name"]
    assert db_product["description"] == payload["description"]
    assert db_product["price"] == payload["price"]
    assert db_product["category"] == payload["category"]

def test_get_existing_product(product_api):
    unique_id = uuid.uuid4().hex[:8]

    payload = {
        "name": f"Phone_{unique_id}",
        "description": "QA Test Phone",
        "price": 50000,
        "category": "Electronics",
    }

    create_response = product_api.create_product(payload)
    

    assert create_response.status_code == 201

    product_id = create_response.json()["id"]

    response = product_api.get_product(product_id)
    

    assert response.status_code == 200

    data = response.json()

    assert data["id"] == product_id
    assert data["name"] == payload["name"]
    assert data["description"] == payload["description"]
    assert data["price"] == payload["price"]
    assert data["category"] == payload["category"]


def test_get_nonexistent_product(product_api):
    response = product_api.get_product(999999)
    

    assert response.status_code == 404
    assert response.json()["detail"] == "Product not found"

def test_create_product_missing_name(product_api):
    payload = {
        "description": "Product without name",
        "price": 1000,
        "category": "Test",
    }

    response = product_api.create_product(payload)
    

    assert response.status_code == 422


def test_create_product_missing_category(product_api):
    payload = {
        "name": "Product without category",
        "description": "Product without category",
        "price": 1000,
    }

    response = product_api.create_product(payload)
    

    assert response.status_code == 422