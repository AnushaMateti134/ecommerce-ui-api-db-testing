from playwright.sync_api import Page


class CheckoutPage:
    def __init__(self, page: Page):
        self.page = page

        self.first_name_input = page.locator(
            '[data-testid="first-name"]'
        )

        self.last_name_input = page.locator(
            '[data-testid="last-name"]'
        )

        self.address_input = page.locator(
            '[data-testid="address"]'
        )

        self.place_order_button = page.locator(
            '[data-testid="place-order"]'
        )

        self.order_confirmation = page.locator(
            '[data-testid="order-confirmation"]'
        )

    def fill_customer_details(
        self,
        first_name: str,
        last_name: str,
        address: str,
    ):
        self.first_name_input.fill(first_name)
        self.last_name_input.fill(last_name)
        self.address_input.fill(address)

    def place_order(self):
        self.place_order_button.click()

    def get_confirmation_message(self) -> str:
        return self.order_confirmation.inner_text()