@echo off
setlocal

echo Running Jenkins pipeline steps locally...

python -c "from generate_allure_report import cleanup_report_session; cleanup_report_session()"
python -m pip install --upgrade pip
python -m pip install playwright pytest pytest-playwright allure-pytest
python -m playwright install chromium
call npm install allure-commandline --save-dev
python -m pytest tests/test_signup_login.py -v --headed

echo.
echo Allure HTML report:
echo reports\html\allure-report\index.html

endlocal
