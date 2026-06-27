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

Report folder:

```
reports/html/allure-report/index.html
```

**Important:** Do not open `index.html` directly from File Explorer.  
Browsers block Allure data loading from `file://` and show **Failed to fetch**.

Open the report using a local server:

```bash
python generate_allure_report.py --open
```

Or double-click:

```
open-allure-report.bat
```

## Jenkins integration

Full Jenkins setup guide: [`jenkins/README.md`](jenkins/README.md)

### Quick setup

1. Install plugins listed in `jenkins/plugins.txt`
2. Create Pipeline job `VavniServices-Playwright`
3. Use SCM: `https://github.com/kunalpipaliya1/VavniServices.git`
4. Script Path: `Jenkinsfile`

### Schedule

| Trigger | When |
|---|---|
| Cron | Daily at 9:00 AM |
| Poll SCM | Every 15 minutes |

### Jenkins pipeline stages

1. Checkout
2. Clean Old Reports
3. Install Dependencies
4. Health Check (`/login`, `/register`)
5. Run Playwright Tests
6. Publish Allure HTML + JUnit

### Manual run locally (same steps as Jenkins)

```bat
jenkins\run-local.bat
```

## Repository

https://github.com/kunalpipaliya1/VavniServices.git
