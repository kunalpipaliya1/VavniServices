import subprocess
from pathlib import Path

import pytest

from generate_allure_report import ALLURE_INDEX_FILE, cleanup_report_session, generate_allure_html_report

HEADLESS = False


def pytest_sessionstart(session: pytest.Session) -> None:
    del session
    cleanup_report_session()
    print("Previous report files removed. Starting new report session.")


def pytest_sessionfinish(session: pytest.Session, exitstatus: int) -> None:
    del session, exitstatus
    try:
        generate_allure_html_report(open_in_chrome=False)
        print(f"Allure report folder: {ALLURE_INDEX_FILE.parent}")
        print("Open report: python generate_allure_report.py --open")
        print("Or double-click: open-allure-report.bat")
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
