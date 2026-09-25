@echo off
setlocal
cd /d "%~dp0backend"
title LegalEase - FastAPI Server

if not exist .venv (
    echo Creating Python virtual environment...
    py -3.13 -m venv .venv
    if errorlevel 1 py -3.12 -m venv .venv
    if errorlevel 1 (
        echo.
        echo ERROR: Could not create the virtual environment.
        echo Install Python 3.12 or newer and make sure the Python launcher is available.
        pause
        exit /b 1
    )
)

call .venv\Scripts\activate.bat
if errorlevel 1 (
    echo ERROR: Could not activate the virtual environment.
    pause
    exit /b 1
)

python -m pip install --upgrade pip setuptools wheel
if errorlevel 1 (
    echo ERROR: pip upgrade failed.
    pause
    exit /b 1
)

python -m pip install -r requirements.txt
if errorlevel 1 (
    echo.
    echo ERROR: Dependency installation failed.
    echo If you are using Python 3.14 and a package has no wheel yet, install Python 3.13 or 3.12.
    pause
    exit /b 1
)

if not exist .env copy /Y .env.example .env >nul

echo.
echo LegalEase is starting...
echo Open: http://127.0.0.1:8000
 echo.
python -m uvicorn app.main:app --reload
pause
