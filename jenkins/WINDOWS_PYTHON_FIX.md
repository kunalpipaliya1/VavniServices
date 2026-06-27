# Fix: `'python' is not recognized` on Jenkins Windows

Jenkins runs as **SYSTEM** user. If Python was installed for your user only, Jenkins cannot find `python`.

## Fix 1: Install Python for all users (recommended)

1. Download Python 3.12 from https://www.python.org/downloads/
2. Run installer
3. Check **Add python.exe to PATH**
4. Check **Install for all users**
5. Install to: `C:\Program Files\Python312\`
6. Restart Jenkins service:
   ```bat
   net stop Jenkins
   net start Jenkins
   ```

## Fix 2: Use `py` launcher in Jenkins build step

Replace `python` with `py -3`:

```bat
py -3 -m pip install --upgrade pip
py -3 -m pip install playwright pytest pytest-playwright allure-pytest
py -3 -m playwright install chromium
npm install allure-commandline --save-dev
```

## Fix 3: Use project script (easiest)

In Jenkins **Execute Windows batch command**:

```bat
call jenkins\run-jenkins-build.bat
```

This runs cleanup, install, and tests with auto Python detection.

## Fix 4: Set PATH in Jenkins job

**Manage Jenkins** → **System** → **Global properties** → **Environment variables**

| Name | Value |
|---|---|
| `PATH` | `C:\Program Files\Python312;C:\Program Files\Python312\Scripts;C:\Program Files\nodejs;%PATH%` |

Adjust paths to match your Python and Node.js install locations.

## Verify on Jenkins agent

Add a test build step:

```bat
where python
where py
where npm
python --version
py -3 --version
```

If all fail, Python is not installed for the Jenkins SYSTEM user.
