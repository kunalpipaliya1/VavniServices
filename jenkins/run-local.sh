#!/usr/bin/env bash
set -euo pipefail

echo "Running Jenkins pipeline steps locally..."

python3 -c "from generate_allure_report import cleanup_report_session; cleanup_report_session()"
python3 -m pip install -r requirements.txt
python3 -m playwright install chromium
npm install

export DISPLAY=:99
Xvfb :99 -screen 0 1920x1080x24 >/dev/null 2>&1 &
sleep 2

python3 -m pytest tests/test_signup_login.py -v --headed

echo
echo "Allure HTML report:"
echo "reports/html/allure-report/index.html"
