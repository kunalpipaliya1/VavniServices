@echo off
setlocal enabledelayedexpansion

echo Detecting Python...

set "PYTHON_CMD="

where py >nul 2>&1
if !errorlevel!==0 (
    set "PYTHON_CMD=py -3"
    goto :found_python
)

for %%P in (
    "C:\Program Files\Python312\python.exe"
    "C:\Program Files\Python311\python.exe"
    "C:\Program Files\Python310\python.exe"
    "C:\Users\ozakr\AppData\Local\Programs\Python\Python312\python.exe"
) do (
    if exist %%P (
        set "PYTHON_CMD=%%~P"
        goto :found_python
    )
)

echo ERROR: Python not found.
exit /b 1

:found_python
echo Using Python: !PYTHON_CMD!

!PYTHON_CMD! -c "from generate_allure_report import cleanup_report_session; cleanup_report_session()"
if errorlevel 1 exit /b 1

call jenkins\install-deps.bat
if errorlevel 1 exit /b 1

!PYTHON_CMD! -m pytest tests/test_signup_login.py -v --headed
if errorlevel 1 exit /b 1

echo.
echo Allure HTML report folder:
echo reports\html\allure-report\index.html
exit /b 0
