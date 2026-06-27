@echo off
cd /d "%~dp0"
python generate_allure_report.py --open
