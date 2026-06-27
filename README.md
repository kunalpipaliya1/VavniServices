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

Old report files are removed automatically before each new test session.

## Jenkins integration

### 1. Create Pipeline job

1. Open Jenkins → **New Item**
2. Name: `VavniServices-Playwright`
3. Type: **Pipeline** → OK
4. Under **Pipeline**:
   - Definition: **Pipeline script from SCM**
   - SCM: **Git**
   - Repository URL: `https://github.com/kunalpipaliya1/VavniServices.git`
   - Branch: `*/main`
   - Script Path: `Jenkinsfile`
5. Save

### 2. Required Jenkins plugins

- Pipeline
- Git
- HTML Publisher
- JUnit

### 3. Schedule

The `Jenkinsfile` runs the job daily at **9:00 AM** (Jenkins server time):

```groovy
triggers {
    cron('H 9 * * *')
}
```

Change the cron expression in `Jenkinsfile` if you need a different schedule.

Examples:

| Schedule | Cron |
|---|---|
| Every day at 9 AM | `H 9 * * *` |
| Every 6 hours | `H */6 * * *` |
| Weekdays at 8 AM | `H 8 * * 1-5` |
| Every Monday at 7 AM | `H 7 * * 1` |

### 4. Manual run

Click **Build with Parameters** and set `BASE_URL` if the app URL is different from `http://localhost:3001`.

### 5. Reports in Jenkins

After each build:

- **Allure HTML Report** link on the build page
- Archived artifacts in `reports/html/allure-report/`
- JUnit results in build summary

## Repository

https://github.com/kunalpipaliya1/VavniServices.git
