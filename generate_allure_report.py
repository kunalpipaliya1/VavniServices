import shutil
import subprocess
import sys
import threading
import webbrowser
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent
REPORTS_DIR = PROJECT_ROOT / "reports"
ALLURE_RESULTS_DIR = REPORTS_DIR / "allure"
HTML_DIR = REPORTS_DIR / "html"
ALLURE_HTML_DIR = HTML_DIR / "allure-report"
ALLURE_INDEX_FILE = ALLURE_HTML_DIR / "index.html"
JUNIT_DIR = REPORTS_DIR / "junit"
ALLURE_CMD = PROJECT_ROOT / "node_modules" / ".bin" / "allure.cmd"
DEFAULT_REPORT_PORT = 8765


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
    print(f"Report folder: {ALLURE_HTML_DIR}")
    print(f"Report file:   {ALLURE_INDEX_FILE}")
    print("Do not open index.html directly from Explorer.")
    print("Use: python generate_allure_report.py --open")
    print("=" * 40)

    if open_in_chrome:
        open_report_in_chrome()

    return ALLURE_INDEX_FILE


def get_report_url(port: int = DEFAULT_REPORT_PORT) -> str:
    return f"http://127.0.0.1:{port}/index.html"


def open_report_in_chrome(port: int = DEFAULT_REPORT_PORT) -> str:
    if not ALLURE_INDEX_FILE.exists():
        raise FileNotFoundError(
            f"Allure report not found at {ALLURE_INDEX_FILE}. Generate it first."
        )

    report_url = get_report_url(port)
    server = ThreadingHTTPServer(
        ("127.0.0.1", port),
        lambda *args, **kwargs: SimpleHTTPRequestHandler(
            *args,
            directory=str(ALLURE_HTML_DIR),
            **kwargs,
        ),
    )
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()

    chrome_paths = [
        Path(r"C:\Program Files\Google\Chrome\Application\chrome.exe"),
        Path(r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe"),
        Path.home() / "AppData" / "Local" / "Google" / "Chrome" / "Application" / "chrome.exe",
    ]
    chrome_exe = next((path for path in chrome_paths if path.exists()), None)

    if chrome_exe:
        subprocess.Popen([str(chrome_exe), report_url])
    else:
        webbrowser.open(report_url)

    print(f"Allure report opened at: {report_url}")
    print("Keep this window open while viewing the report.")
    return report_url


def main() -> None:
    open_in_chrome = "--open" in sys.argv or "-o" in sys.argv

    if ALLURE_INDEX_FILE.exists() and not (
        ALLURE_RESULTS_DIR.exists() and any(ALLURE_RESULTS_DIR.iterdir())
    ):
        if open_in_chrome:
            open_report_in_chrome()
            input("Press Enter to stop report server...")
        else:
            print(f"Existing report: {ALLURE_INDEX_FILE}")
            print("Open with: python generate_allure_report.py --open")
        return

    generate_allure_html_report(open_in_chrome=open_in_chrome)

    if open_in_chrome:
        input("Press Enter to stop report server...")


if __name__ == "__main__":
    main()
