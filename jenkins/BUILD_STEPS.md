# Jenkins Build Steps

## Option A: Pipeline job (recommended)

Use the `Jenkinsfile` from the repo. No manual build steps needed.

### Job configuration

| Setting | Value |
|---|---|
| Job type | Pipeline |
| Definition | Pipeline script from SCM |
| SCM | Git |
| Repository URL | `https://github.com/kunalpipaliya1/VavniServices.git` |
| Branch | `*/main` |
| Script Path | `Jenkinsfile` |

### Pipeline stages (automatic)

| # | Stage | What it does |
|---|---|---|
| 1 | Checkout | Pull code from GitHub |
| 2 | Clean Old Reports | Remove old Allure/JUnit files |
| 3 | Install Dependencies | pip, Playwright, npm |
| 4 | Health Check | Verify `/login` and `/register` |
| 5 | Run Playwright Tests | Run pytest with Allure report |
| 6 | Post-build | Publish Allure HTML + JUnit |

### Build parameters

| Parameter | Default |
|---|---|
| `BASE_URL` | `http://localhost:3001` |
| `BROWSER` | `chromium` |

---

## Option B: Freestyle job (manual build steps)

Use this if you are not using Pipeline.

### Job configuration

| Setting | Value |
|---|---|
| Job type | Freestyle project |
| Source Code Management | Git → `https://github.com/kunalpipaliya1/VavniServices.git` |
| Branch | `*/main` |

### Build Triggers

- Build periodically: `H 9 * * *` (daily 9 AM)
- Poll SCM: `H/15 * * * *` (every 15 minutes)

---

### Windows agent — Execute Windows batch command

**Build Step 1: Clean old reports**
```bat
python -c "from generate_allure_report import cleanup_report_session; cleanup_report_session()"
```

**Build Step 2: Install dependencies**

Use the script (recommended):
```bat
call jenkins\install-deps.bat
```

Or paste manually after fixing Python path:
```bat
py -3 -m pip install --upgrade pip
py -3 -m pip install playwright pytest pytest-playwright allure-pytest
py -3 -m playwright install chromium
npm install allure-commandline --save-dev
```

If `py` is not found, use full path:
```bat
"C:\Program Files\Python312\python.exe" -m pip install --upgrade pip
"C:\Program Files\Python312\python.exe" -m pip install playwright pytest pytest-playwright allure-pytest
"C:\Program Files\Python312\python.exe" -m playwright install chromium
npm install allure-commandline --save-dev
```

**Build Step 3: Health check**
```bat
python -c "import os,sys,urllib.request; base=os.environ.get('BASE_URL','http://localhost:3001');
for path in ['/login','/register']:
 url=base+path
 try:
  r=urllib.request.urlopen(url,timeout=20); print(url,'->',r.status)
 except Exception as e:
  print(url,'is not reachable:',e); sys.exit(1)"
```

**Build Step 4: Run tests**
```bat
python -m pytest tests/test_signup_login.py -v --headed
```

---

### Linux agent — Execute shell

**Build Step 1: Clean old reports**
```bash
python3 -c "from generate_allure_report import cleanup_report_session; cleanup_report_session()"
```

**Build Step 2: Install dependencies**
```bash
python3 -m pip install --upgrade pip
python3 -m pip install playwright pytest pytest-playwright allure-pytest
python3 -m playwright install chromium
npm install allure-commandline --save-dev
```

**Build Step 3: Health check**
```bash
python3 - <<'PY'
import os
import sys
import urllib.request

base_url = os.environ.get("BASE_URL", "http://localhost:3001")
for path in ("/login", "/register"):
    url = f"{base_url}{path}"
    try:
        with urllib.request.urlopen(url, timeout=20) as response:
            print(f"{url} -> {response.status}")
    except Exception as error:
        print(f"{url} is not reachable: {error}")
        sys.exit(1)
PY
```

**Build Step 4: Run tests**
```bash
export DISPLAY=:99
Xvfb :99 -screen 0 1920x1080x24 > /dev/null 2>&1 &
sleep 2
python3 -m pytest tests/test_signup_login.py -v --headed
```

---

## Post-build actions (Freestyle)

Add these after the build steps:

### 1. Archive the artifacts
```
reports/html/allure-report/**
reports/junit/results.xml
```

### 2. Publish HTML report
| Setting | Value |
|---|---|
| HTML directory to archive | `reports/html/allure-report` |
| Index page | `index.html` |
| Report title | `Allure HTML Report` |

### 3. Publish JUnit test result report
```
reports/junit/results.xml
```

---

## Required Jenkins plugins

```
workflow-aggregator
git
github
pipeline-stage-view
timestamps
build-timeout
htmlpublisher
junit
ws-cleanup
schedule-build
```

Install from: **Manage Jenkins** → **Plugins** → list in `jenkins/plugins.txt`

---

## After build — view report

On the build page click:

- **Allure HTML Report** (left side menu)
- **Test Result** for pass/fail summary

Report path on Jenkins server:
```
${WORKSPACE}/reports/html/allure-report/index.html
```
