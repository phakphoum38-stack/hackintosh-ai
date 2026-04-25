from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from backend.core.security import create_token

router = APIRouter()

# =========================
# 🔐 Request Schema
# =========================
class LoginRequest(BaseModel):
    id: str
    tenant_id: str

# =========================
# 🔐 Login API
# =========================
@router.post("/login")
def login(user: LoginRequest):

    if not user.id or not user.tenant_id:
        raise HTTPException(status_code=400, detail="Missing credentials")

    token = create_token({
        "user_id": user.id,
        "tenant_id": user.tenant_id
    })

    return {
        "access_token": token,
        "token_type": "bearer"
    }
