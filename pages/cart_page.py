from playwright.sync_api import Page


class CartPage:
    def __init__(self, page: Page):
        self.page = page

        self.cart_items = page.locator(
            '[data-testid="cart-item"]'
        )

        self.checkout_button = page.locator(
            '[data-testid="checkout-button"]'
        )

        self.cart_total = page.locator(
            '[data-testid="cart-total"]'
        )

    def get_item_count(self) -> int:
        return self.cart_items.count()

    def get_item(self, product_name: str):
        return self.cart_items.filter(
            has_text=product_name
        )

    def get_total(self) -> str:
        return self.cart_total.inner_text()

    def proceed_to_checkout(self):
        self.checkout_button.click()