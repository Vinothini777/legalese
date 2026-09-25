# LegalEase - HTML/CSS/JavaScript + FastAPI

A non-React LegalEase project using:

- HTML5
- CSS3
- Vanilla JavaScript
- Python FastAPI
- SQLite + SQLAlchemy
- JWT authentication
- Optional Google Gemini API

## Run on Windows

1. Install Python 3.12 or 3.13 if possible.
2. Extract the project.
3. Double-click `run.bat`.
4. Open `http://127.0.0.1:8000`.

### Manual commands

```powershell
cd LegalEase_HTML_CSS_JS\backend
py -m venv .venv
.venv\Scripts\activate
python -m pip install --upgrade pip setuptools wheel
python -m pip install -r requirements.txt
copy .env.example .env
python -m uvicorn app.main:app --reload
```

## Features

- Register and login
- JWT-protected user account
- AI legal-information assistant
- Analysis history
- Document create/edit/delete workspace
- SQLite database
- Gemini integration when `GEMINI_API_KEY` is configured
- Demo legal-information response when Gemini is not configured

## Important

This is an educational project. It does not provide professional legal advice.
