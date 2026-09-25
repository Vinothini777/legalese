from pathlib import Path
from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from .database import init_db
from .routes.auth import router as auth_router
from .routes.analysis import router as analysis_router
from .routes.documents import router as documents_router

BASE_DIR = Path(__file__).resolve().parents[2]
FRONTEND_DIR = BASE_DIR / "frontend"
init_db()

app = FastAPI(title="LegalEase", version="2.0.0", description="AI legal information assistant")
app.include_router(auth_router)
app.include_router(analysis_router)
app.include_router(documents_router)


@app.get("/api/health")
def health():
    return {"status": "ok", "service": "LegalEase", "database": "sqlite3"}


@app.get("/", include_in_schema=False)
def home():
    return FileResponse(FRONTEND_DIR / "index.html")


app.mount("/static", StaticFiles(directory=FRONTEND_DIR), name="static")
