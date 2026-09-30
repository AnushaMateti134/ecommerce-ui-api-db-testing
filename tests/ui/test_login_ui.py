from playwright.sync_api import Page, expect

from pages.login_page import LoginPage


def test_login_page_loads(page: Page):
    login_page = LoginPage(page)

    login_page.open()

    expect(
        login_page.username_input
    ).to_be_visible()

    expect(
        login_page.email_input
    ).to_be_visible()

    expect(
        login_page.password_input
    ).to_be_visible()

    expect(
        login_page.login_button
    ).to_be_visible()