from fastapi import APIRouter, Depends
from datetime import datetime, timezone
from ..ai import generate_legal_response
from ..database import get_connection, row_to_dict
from ..schemas import AnalysisCreate, AnalysisResponse
from ..security import get_current_user

router = APIRouter(prefix="/api/analysis", tags=["AI Analysis"])


def now_iso():
    return datetime.now(timezone.utc).isoformat()


@router.get("", response_model=list[AnalysisResponse])
def list_analysis(user=Depends(get_current_user)):
    with get_connection() as conn:
        rows = conn.execute("SELECT id,title,issue,category,response,created_at FROM analyses WHERE user_id=? ORDER BY created_at DESC", (user["id"],)).fetchall()
    return [row_to_dict(r) for r in rows]


@router.post("", response_model=AnalysisResponse)
def create_analysis(data: AnalysisCreate, user=Depends(get_current_user)):
    issue = data.issue.strip()
    category = data.category.strip() or "General"
    title = data.title.strip() or "Legal Analysis"
    response = generate_legal_response(issue, category)
    created = now_iso()
    with get_connection() as conn:
        cur = conn.execute("INSERT INTO analyses(user_id,title,issue,category,response,created_at) VALUES(?,?,?,?,?,?)", (user["id"], title, issue, category, response, created))
        item = row_to_dict(conn.execute("SELECT id,title,issue,category,response,created_at FROM analyses WHERE id=?", (cur.lastrowid,)).fetchone())
    return item
