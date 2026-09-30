from playwright.sync_api import Page


class ProductsPage:
    def __init__(self, page: Page):
        self.page = page

        self.product_list = page.locator(
            '[data-testid="product-list"]'
        )

        self.product_items = page.locator(
            '[data-testid="product-item"]'
        )

        self.cart_button = page.locator(
            '[data-testid="cart-button"]'
        )

    def get_product_count(self) -> int:
        return self.product_items.count()

    def add_product_to_cart(self, product_name: str):
        product = self.product_items.filter(
        has=self.page.locator("h3").filter(
            has_text=product_name
        )
        ).first

        product.locator(
        '[data-testid="add-to-cart"]'
        ).click()

    def open_cart(self):
        self.cart_button.click()