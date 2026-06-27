import subprocess
import sys
from pathlib import Path

import pytest

from generate_allure_report import ALLURE_INDEX_FILE, generate_allure_html_report

REPORTS_DIR = Path(__file__).resolve().parent / "reports"
ALLURE_DIR = REPORTS_DIR / "allure"
HTML_DIR = REPORTS_DIR / "html"
HEADLESS = False


@pytest.fixture(scope="session", autouse=True)
def setup_report_dirs() -> None:
    ALLURE_DIR.mkdir(parents=True, exist_ok=True)
    HTML_DIR.mkdir(parents=True, exist_ok=True)


def pytest_sessionfinish(session: pytest.Session, exitstatus: int) -> None:
    del session, exitstatus
    try:
        generate_allure_html_report(open_in_chrome=False)
        print(f"Open Allure report in Chrome: {ALLURE_INDEX_FILE.resolve().as_uri()}")
    except (FileNotFoundError, subprocess.CalledProcessError) as error:
        print(f"Allure HTML report was not generated: {error}")


@pytest.fixture(scope="session")
def browser_type_launch_args(browser_type_launch_args: dict[str, object]) -> dict[str, object]:
    return {
        **browser_type_launch_args,
        "headless": HEADLESS,
        "args": ["--start-maximized"],
    }


@pytest.fixture(scope="session")
def browser_context_args(browser_context_args: dict[str, object]) -> dict[str, object]:
    return {
        **browser_context_args,
        "no_viewport": True,
    }
