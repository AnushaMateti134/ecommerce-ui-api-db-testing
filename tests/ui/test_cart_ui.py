from playwright.sync_api import Page, expect

from pages.products_page import ProductsPage
from pages.cart_page import CartPage


def test_add_product_to_cart(page: Page):
    products_page = ProductsPage(page)
    cart_page = CartPage(page)

    page.goto("/frontend/products.html")

    expect(
        products_page.product_items.first
    ).to_be_visible()

    product = products_page.product_items.first
    product_name = product.locator("h3").inner_text()

    products_page.add_product_to_cart(product_name)

    products_page.open_cart()

    expect(
        cart_page.cart_items.first
    ).to_be_visible()

    assert cart_page.get_item_count() == 1

    expect(
        cart_page.get_item(product_name)
    ).to_be_visible()