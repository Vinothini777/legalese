from fastapi import APIRouter, HTTPException, status, Depends
from ..database import get_connection, row_to_dict
from ..schemas import LoginRequest, RegisterRequest, TokenResponse, UserResponse
from ..security import create_access_token, get_current_user, hash_password, verify_password
from datetime import datetime, timezone

router = APIRouter(prefix="/api/auth", tags=["Authentication"])


def now_iso():
    return datetime.now(timezone.utc).isoformat()


@router.post("/register", response_model=TokenResponse, status_code=status.HTTP_201_CREATED)
def register(data: RegisterRequest):
    name = data.name.strip()
    email = str(data.email).lower().strip()
    if len(name) < 2:
        raise HTTPException(status_code=400, detail="Name must contain at least 2 characters")
    with get_connection() as conn:
        exists = conn.execute("SELECT id FROM users WHERE email = ?", (email,)).fetchone()
        if exists:
            raise HTTPException(status_code=409, detail="Email is already registered")
        cur = conn.execute("INSERT INTO users(name,email,password_hash,created_at) VALUES(?,?,?,?)", (name, email, hash_password(data.password), now_iso()))
        user_id = cur.lastrowid
    return TokenResponse(access_token=create_access_token(user_id))


@router.post("/login", response_model=TokenResponse)
def login(data: LoginRequest):
    email = str(data.email).lower().strip()
    with get_connection() as conn:
        user = row_to_dict(conn.execute("SELECT * FROM users WHERE email = ?", (email,)).fetchone())
    if not user or not verify_password(data.password, user["password_hash"]):
        raise HTTPException(status_code=401, detail="Invalid email or password")
    return TokenResponse(access_token=create_access_token(user["id"]))


@router.get("/me", response_model=UserResponse)
def me(user = Depends(get_current_user)):
    return user
