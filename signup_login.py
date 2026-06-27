from pathlib import Path

from playwright.sync_api import Page, sync_playwright

BASE_URL = "http://localhost:3001"
REGISTER_URL = f"{BASE_URL}/register"
LOGIN_URL = f"{BASE_URL}/login"
USERNAME = "kunal@test.com"
PASSWORD = "Password@123"
OTP = "000000"
EXPECTED_PAGE_TITLE = "OnRule"
HEADLESS = False

REPORTS_DIR = Path(__file__).resolve().parent / "reports"
ALLURE_DIR = REPORTS_DIR / "allure"
HTML_DIR = REPORTS_DIR / "html"


def ensure_report_dirs() -> None:
    ALLURE_DIR.mkdir(parents=True, exist_ok=True)
    HTML_DIR.mkdir(parents=True, exist_ok=True)


def get_notification_count(page: Page, label: str) -> int:
    count_locator = page.locator(
        f'xpath=//p[normalize-space()="{label}"]/preceding-sibling::h4[1]'
    )
    count_locator.first.wait_for(state="visible", timeout=30000)
    return int(count_locator.first.inner_text())


def verify_home_page(page: Page) -> dict[str, int]:
    page.wait_for_url("**/home**", timeout=30000)
    page.wait_for_load_state("domcontentloaded")
    page.locator('xpath=//p[normalize-space()="Total"]').first.wait_for(
        state="visible",
        timeout=30000,
    )

    assert "/home" in page.url, f"Expected home URL, got: {page.url}"
    assert page.title() == EXPECTED_PAGE_TITLE, (
        f"Expected title '{EXPECTED_PAGE_TITLE}', got: '{page.title()}'"
    )

    counts: dict[str, int] = {
        "total": get_notification_count(page, "Total"),
        "unread": get_notification_count(page, "Unread"),
        "important": get_notification_count(page, "Important"),
    }

    print("=" * 40)
    print("HOME PAGE VERIFIED")
    print(f"Page Title: {page.title()}")
    print(f"Current URL: {page.url}")
    print(f"Total Notifications: {counts['total']}")
    print(f"Unread Notifications: {counts['unread']}")
    print(f"Important Notifications: {counts['important']}")
    print("=" * 40)

    return counts


def enter_otp_and_verify(page: Page, otp: str = OTP) -> dict[str, int]:
    otp_inputs = page.locator('xpath=//input[@type="tel"]')
    otp_inputs.first.wait_for(state="visible", timeout=30000)
    otp_inputs.first.fill(otp)
    page.locator('xpath=//button[normalize-space()="Verify & Login"]').click()
    return verify_home_page(page)


def create_account(page: Page) -> None:
    page.goto(REGISTER_URL, wait_until="domcontentloaded")
    page.locator('xpath=//input[@name="firstname"]').wait_for(state="visible")

    page.locator('xpath=//input[@name="firstname"]').fill("Kunal")
    page.locator('xpath=//input[@name="lastname"]').fill("Pipaliya")
    page.locator('xpath=//input[@name="email"]').fill(USERNAME)
    page.locator('xpath=//input[@name="password"]').fill(PASSWORD)
    page.locator('xpath=//input[@name="confirmPassword"]').fill(PASSWORD)

    page.locator('xpath=//button[normalize-space()="Create Account"]').click()
    page.wait_for_timeout(3000)

    print("=" * 40)
    print("ACCOUNT CREATED")
    print(f"Username: {USERNAME}")
    print(f"Password: {PASSWORD}")
    print(f"Current URL: {page.url}")
    print("=" * 40)


def login(page: Page) -> dict[str, int]:
    page.goto(LOGIN_URL, wait_until="domcontentloaded")
    page.locator('xpath=//input[@name="email"]').wait_for(state="visible")

    page.locator('xpath=//input[@name="email"]').fill(USERNAME)
    page.locator('xpath=//input[@name="password"]').fill(PASSWORD)
    page.locator('xpath=//button[normalize-space()="Login"]').click()

    notification_counts: dict[str, int] = enter_otp_and_verify(page)

    print("=" * 40)
    print("LOGGED IN")
    print(f"Username: {USERNAME}")
    print(f"Password: {PASSWORD}")
    print(f"OTP: {OTP}")
    print(f"Current URL: {page.url}")
    print(f"Total Notifications: {notification_counts['total']}")
    print(f"Unread Notifications: {notification_counts['unread']}")
    print(f"Important Notifications: {notification_counts['important']}")
    print("=" * 40)

    return notification_counts


def run_signup_login_flow() -> None:
    ensure_report_dirs()

    with sync_playwright() as playwright:
        browser = playwright.chromium.launch(
            headless=HEADLESS,
            args=["--start-maximized"],
        )
        page = browser.new_page(no_viewport=True)

        try:
            create_account(page)
            login(page)
        finally:
            page.wait_for_timeout(2000)
            browser.close()


def main() -> None:
    run_signup_login_flow()


if __name__ == "__main__":
    main()
