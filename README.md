# VavniServices

Playwright automation for signup, login with OTP, and Allure HTML reporting.

## Setup

```bash
pip install -r requirements.txt
playwright install chromium
npm install
```

## Run tests

```bash
python -m pytest tests/test_signup_login.py -v
```

## Allure HTML report

After tests, open:

```
reports/html/allure-report/index.html
```

Or generate manually:

```bash
python generate_allure_report.py --open
```

## Jenkins

Use the included `Jenkinsfile` for CI pipeline execution.
