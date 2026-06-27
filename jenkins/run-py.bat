@echo off
setlocal enabledelayedexpansion

set "PYTHON_CMD="

where py >nul 2>&1
if !errorlevel!==0 (
    set "PYTHON_CMD=py -3"
    goto :run
)

for %%P in (
    "C:\Program Files\Python312\python.exe"
    "C:\Program Files\Python311\python.exe"
    "C:\Program Files\Python310\python.exe"
    "C:\Users\ozakr\AppData\Local\Programs\Python\Python312\python.exe"
) do (
    if exist %%P (
        set "PYTHON_CMD=%%~P"
        goto :run
    )
)

echo ERROR: Python not found.
exit /b 1

:run
!PYTHON_CMD! %*
exit /b !errorlevel!
