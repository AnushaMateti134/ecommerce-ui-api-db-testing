import uuid

from playwright.sync_api import Page, expect

from api_clients.user_api import UserAPI
from config.settings import BASE_URL
from db.db_helper import (
    get_order_by_id,
    get_order_items_by_order_id,
)
from pages.products_page import ProductsPage
from pages.cart_page import CartPage
from pages.checkout_page import CheckoutPage


def test_complete_purchase_flow(page: Page):
    # --------------------------------
    # 1. Create test user through API
    # --------------------------------

    user_api = UserAPI(BASE_URL)

    unique_id = uuid.uuid4().hex[:8]

    user_payload = {
        "username": f"e2e_user_{unique_id}",
        "email": f"e2e_{unique_id}@example.com",
        "password": "Test@123",
    }

    user_response = user_api.create_user(user_payload)

    assert user_response.status_code == 201

    user_id = user_response.json()["id"]

    # --------------------------------
    # 2. Open Products page
    # --------------------------------

    products_page = ProductsPage(page)
    cart_page = CartPage(page)
    checkout_page = CheckoutPage(page)

    page.goto("/frontend/products.html")

    expect(
        products_page.product_items.first
    ).to_be_visible()

    # --------------------------------
    # 3. Add product to cart
    # --------------------------------

    product = products_page.product_items.first

    product_name = (
        product.locator("h3").inner_text()
    )

    products_page.add_product_to_cart(
        product_name
    )

    # --------------------------------
    # 4. Verify cart
    # --------------------------------

    products_page.open_cart()

    expect(
        cart_page.cart_items.first
    ).to_be_visible()

    assert cart_page.get_item_count() == 1

    expect(
        cart_page.get_item(product_name)
    ).to_be_visible()

    # --------------------------------
    # 5. Go to checkout
    # --------------------------------

    cart_page.proceed_to_checkout()

    expect(
        checkout_page.first_name_input
    ).to_be_visible()

    # --------------------------------
    # 6. Set browser user session
    # --------------------------------

    page.evaluate(
        """(user_id) => {
            sessionStorage.setItem(
                "userId",
                String(user_id)
            );
        }""",
        user_id
    )

    # --------------------------------
    # 7. Fill customer details
    # --------------------------------

    checkout_page.fill_customer_details(
        first_name="Anusha",
        last_name="Mateti",
        address="QA Test Address"
    )

    # --------------------------------
    # 8. Place order
    # --------------------------------

    checkout_page.place_order()

    expect(
        checkout_page.order_confirmation
    ).to_contain_text(
        "Order placed successfully"
    )

    # --------------------------------
    # 9. Extract Order ID
    # --------------------------------

    confirmation_text = (
        checkout_page.get_confirmation_message()
    )

    order_id = int(
        confirmation_text
        .split("Order ID:")[1]
        .strip()
    )

    # --------------------------------
    # 10. Validate Order in DB
    # --------------------------------

    db_order = get_order_by_id(order_id)

    assert db_order is not None
    assert db_order["id"] == order_id
    assert db_order["user_id"] == user_id
    assert db_order["status"] == "created"

    # --------------------------------
    # 11. Validate Order Item in DB
    # --------------------------------

    db_items = get_order_items_by_order_id(
        order_id
    )

    assert len(db_items) == 1

    db_item = db_items[0]

    assert db_item["order_id"] == order_id
    assert db_item["quantity"] == 1
    assert db_item["price"] > 0