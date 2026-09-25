# Phase 3: Design Phase

Project: LegalEase - AI Legal Document Assistant

## System Architecture Diagram:
User (Browser) -> Frontend (HTML/CSS/JS) -> Backend API (FastAPI) -> 
1. Gemini AI API for Chatbot
2. SQLite Database for User & History
3. PDF Generator

## UI Design (Wireframes):

1. Home Page:
- Navbar: Logo, Login/Register
- Hero Section: "AI Legal Assistant"
- Features: Chatbot, Document Generator

2. Dashboard Page:
- Sidebar: Chat History, My Documents
- Main Area: Chat Window + Document Templates

3. Document Generator Page:
- Form: Name, Address, Terms
- Preview Area
- Download PDF Button

## Database Design:

Table: Users
- id, username, email, password_hash

Table: Chat_History
- id, user_id, question, answer, timestamp

Table: Documents
- id, user_id, doc_type, content, created_at

## Technology Stack:
- Frontend: HTML, CSS, JS
- Backend: FastAPI
- DB: SQLite
- AI: Gemini API
