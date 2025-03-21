@echo off
echo [INFO] Activating virtual environment...

:: Get the full path to the script directory
set SCRIPT_DIR=%~dp0
cd /d %SCRIPT_DIR%

echo [%DATE% %TIME%] Starting... >> refresher.log

:: Activate virtual environment
call .venv\Scripts\activate.bat

:: Run the token refresher
python token_refresher\token_refresher.py

echo [%DATE% %TIME%] Done. >> refresher.log

exit /b 0
