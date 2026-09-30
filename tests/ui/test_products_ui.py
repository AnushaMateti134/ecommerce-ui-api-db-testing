from playwright.sync_api import Page, expect

from pages.products_page import ProductsPage


def test_products_page_displays_products(page: Page):
    products_page = ProductsPage(page)

    page.goto("/frontend/products.html")

    expect(
        products_page.product_list
    ).to_be_visible()

    expect(
        products_page.product_items.first
    ).to_be_visible()

    assert products_page.get_product_count() > 0