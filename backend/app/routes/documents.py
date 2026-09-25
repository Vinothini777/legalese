from fastapi import APIRouter, Depends, HTTPException
from datetime import datetime, timezone
from ..database import get_connection, row_to_dict
from ..schemas import DocumentCreate, DocumentResponse
from ..security import get_current_user

router = APIRouter(prefix="/api/documents", tags=["Documents"])


def now_iso():
    return datetime.now(timezone.utc).isoformat()


def owned_document(document_id: int, user_id: int):
    with get_connection() as conn:
        row = conn.execute("SELECT * FROM documents WHERE id=? AND user_id=?", (document_id, user_id)).fetchone()
    if not row:
        raise HTTPException(status_code=404, detail="Document not found")
    return row_to_dict(row)


@router.get("", response_model=list[DocumentResponse])
def list_documents(user=Depends(get_current_user)):
    with get_connection() as conn:
        rows = conn.execute("SELECT id,title,content,created_at,updated_at FROM documents WHERE user_id=? ORDER BY updated_at DESC", (user["id"],)).fetchall()
    return [row_to_dict(r) for r in rows]


@router.post("", response_model=DocumentResponse, status_code=201)
def create_document(data: DocumentCreate, user=Depends(get_current_user)):
    title = data.title.strip() or "Untitled Document"
    created = now_iso()
    with get_connection() as conn:
        cur = conn.execute("INSERT INTO documents(user_id,title,content,created_at,updated_at) VALUES(?,?,?,?,?)", (user["id"], title, data.content, created, created))
        return row_to_dict(conn.execute("SELECT id,title,content,created_at,updated_at FROM documents WHERE id=?", (cur.lastrowid,)).fetchone())


@router.put("/{document_id}", response_model=DocumentResponse)
def update_document(document_id: int, data: DocumentCreate, user=Depends(get_current_user)):
    owned_document(document_id, user["id"])
    updated = now_iso()
    with get_connection() as conn:
        conn.execute("UPDATE documents SET title=?, content=?, updated_at=? WHERE id=? AND user_id=?", (data.title.strip() or "Untitled Document", data.content, updated, document_id, user["id"]))
        return row_to_dict(conn.execute("SELECT id,title,content,created_at,updated_at FROM documents WHERE id=?", (document_id,)).fetchone())


@router.delete("/{document_id}")
def delete_document(document_id: int, user=Depends(get_current_user)):
    owned_document(document_id, user["id"])
    with get_connection() as conn:
        conn.execute("DELETE FROM documents WHERE id=? AND user_id=?", (document_id, user["id"]))
    return {"message": "Document deleted"}
