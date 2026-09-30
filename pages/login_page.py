from playwright.sync_api import Page


class LoginPage:
    def __init__(self, page: Page):
        self.page = page

        self.username_input = page.locator(
            '[data-testid="username"]'
        )

        self.email_input = page.locator(
            '[data-testid="email"]'
        )

        self.password_input = page.locator(
            '[data-testid="password"]'
        )

        self.login_button = page.locator(
            '[data-testid="login-button"]'
        )

    def open(self):
        self.page.goto("/frontend/index.html")

    def login(
        self,
        username: str,
        email: str,
        password: str,
    ):
        self.username_input.fill(username)
        self.email_input.fill(email)
        self.password_input.fill(password)
        self.login_button.click()