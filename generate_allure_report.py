import shutil
import subprocess
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent
REPORTS_DIR = PROJECT_ROOT / "reports"
ALLURE_RESULTS_DIR = REPORTS_DIR / "allure"
HTML_DIR = REPORTS_DIR / "html"
ALLURE_HTML_DIR = HTML_DIR / "allure-report"
ALLURE_INDEX_FILE = ALLURE_HTML_DIR / "index.html"
JUNIT_DIR = REPORTS_DIR / "junit"
ALLURE_CMD = PROJECT_ROOT / "node_modules" / ".bin" / "allure.cmd"


def clear_directory(directory: Path) -> None:
    if not directory.exists():
        return

    for item in directory.iterdir():
        if item.is_dir():
            shutil.rmtree(item, ignore_errors=True)
        else:
            try:
                item.unlink()
            except OSError:
                pass


def cleanup_report_session() -> None:
    clear_directory(ALLURE_RESULTS_DIR)
    clear_directory(JUNIT_DIR)

    if ALLURE_HTML_DIR.exists():
        shutil.rmtree(ALLURE_HTML_DIR, ignore_errors=True)

    ALLURE_RESULTS_DIR.mkdir(parents=True, exist_ok=True)
    HTML_DIR.mkdir(parents=True, exist_ok=True)
    JUNIT_DIR.mkdir(parents=True, exist_ok=True)


def cleanup_allure_results() -> None:
    clear_directory(ALLURE_RESULTS_DIR)
    ALLURE_RESULTS_DIR.mkdir(parents=True, exist_ok=True)


def generate_allure_html_report(open_in_chrome: bool = False) -> Path:
    ALLURE_HTML_DIR.mkdir(parents=True, exist_ok=True)

    if not ALLURE_RESULTS_DIR.exists() or not any(ALLURE_RESULTS_DIR.iterdir()):
        raise FileNotFoundError(
            f"No Allure results found in {ALLURE_RESULTS_DIR}. Run pytest first."
        )

    if not ALLURE_CMD.exists():
        raise FileNotFoundError("Allure CLI not found. Run: npm install")

    subprocess.run(
        [
            str(ALLURE_CMD),
            "generate",
            str(ALLURE_RESULTS_DIR),
            "-o",
            str(ALLURE_HTML_DIR),
            "--clean",
        ],
        check=True,
        cwd=PROJECT_ROOT,
    )

    cleanup_allure_results()

    print("=" * 40)
    print("ALLURE HTML REPORT GENERATED")
    print(f"Report path: {ALLURE_INDEX_FILE}")
    print("=" * 40)

    if open_in_chrome:
        open_report_in_chrome()

    return ALLURE_INDEX_FILE


def open_report_in_chrome() -> None:
    if not ALLURE_INDEX_FILE.exists():
        raise FileNotFoundError(
            f"Allure report not found at {ALLURE_INDEX_FILE}. Generate it first."
        )

    chrome_paths = [
        Path(r"C:\Program Files\Google\Chrome\Application\chrome.exe"),
        Path(r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe"),
        Path.home() / "AppData" / "Local" / "Google" / "Chrome" / "Application" / "chrome.exe",
    ]

    chrome_exe = next((path for path in chrome_paths if path.exists()), None)
    report_uri = ALLURE_INDEX_FILE.resolve().as_uri()

    if chrome_exe:
        subprocess.Popen([str(chrome_exe), report_uri])
        print(f"Opened in Chrome: {report_uri}")
        return

    import os

    os.startfile(ALLURE_INDEX_FILE)
    print(f"Opened with default app: {ALLURE_INDEX_FILE}")


def main() -> None:
    open_in_chrome = "--open" in sys.argv or "-o" in sys.argv
    generate_allure_html_report(open_in_chrome=open_in_chrome)


if __name__ == "__main__":
    main()
