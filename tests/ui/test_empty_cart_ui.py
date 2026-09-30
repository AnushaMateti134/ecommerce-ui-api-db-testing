from playwright.sync_api import Page, expect

from pages.cart_page import CartPage


def test_empty_cart_cannot_checkout(page: Page):
    cart_page = CartPage(page)

    page.goto("/frontend/cart.html")

    expect(
        cart_page.cart_items
    ).to_have_count(0)

    expect(
        page.locator("text=Your cart is empty.")
    ).to_be_visible()

    cart_page.checkout_button.click()

    expect(
        page
    ).to_have_url(
        "/frontend/cart.html"
    )