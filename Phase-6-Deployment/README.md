# Phase 6: Deployment Phase

Project: LegalEase - AI Legal Document Assistant

## Deployment Steps:

### 1. Backend Deployment (Render / Railway):
- Pushed backend code to GitHub
- Created new Web Service on Render
- Connected GitHub repo: Vinothini777/legalese
- Set Build Command: pip install -r requirements.txt
- Set Start Command: uvicorn main:app --host 0.0.0.0 --port 10000
- Added Environment Variables: GEMINI_API_KEY, JWT_SECRET
- Deployed backend - Got live API URL

### 2. Frontend Deployment (GitHub Pages / Vercel):
- Updated API base URL in frontend JS to Render backend URL
- Pushed frontend to GitHub
- Enabled GitHub Pages from main branch / frontend folder
- Deployed - Got live website URL

### 3. Database:
- Using SQLite for demo (or PostgreSQL on Render for production)
- Created tables automatically on startup

### 4. Live URLs:
- Frontend: https://vinothini777.github.io/legalese/
- Backend API: https://legalese-api.onrender.com

### 5. Post-Deployment Testing:
- Tested live site registration/login
- Tested chatbot on live site
- Tested PDF download on live site - Working!

## Deployment Tools:
- GitHub for version control
- Render for backend hosting
- GitHub Pages for frontend

## Status: Application is LIVE!
