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
echo Install Python 3.12 for all users and check "Add python.exe to PATH".
exit /b 1

:found_python
echo Using Python: !PYTHON_CMD!

!PYTHON_CMD! -m pip install --upgrade pip
if errorlevel 1 exit /b 1

!PYTHON_CMD! -m pip install playwright pytest pytest-playwright allure-pytest
if errorlevel 1 exit /b 1

!PYTHON_CMD! -m playwright install chromium
if errorlevel 1 exit /b 1

call npm install allure-commandline --save-dev
if errorlevel 1 exit /b 1

echo Dependencies installed successfully.
exit /b 0
