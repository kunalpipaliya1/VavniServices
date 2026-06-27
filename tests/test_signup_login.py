import allure
import pytest
from playwright.sync_api import Page

from signup_login import (
    EXPECTED_PAGE_TITLE,
    OTP,
    PASSWORD,
    USERNAME,
    create_account,
    login,
)


@allure.feature("Authentication")
@allure.story("Signup and Login with OTP")
def test_signup_and_login(page: Page) -> None:
    with allure.step("Create account on register page"):
        create_account(page)
        allure.attach(
            page.url,
            name="URL after signup",
            attachment_type=allure.attachment_type.TEXT,
        )

    with allure.step("Login with OTP verification"):
        notification_counts = login(page)
        allure.attach(
            (
                f"Username: {USERNAME}\n"
                f"Password: {PASSWORD}\n"
                f"OTP: {OTP}\n"
                f"Total Notifications: {notification_counts['total']}\n"
                f"Unread Notifications: {notification_counts['unread']}\n"
                f"Important Notifications: {notification_counts['important']}"
            ),
            name="Login details",
            attachment_type=allure.attachment_type.TEXT,
        )

    assert "/home" in page.url
    assert page.title() == EXPECTED_PAGE_TITLE
    assert notification_counts["total"] >= 0
    assert notification_counts["unread"] >= 0
    assert notification_counts["important"] >= 0
