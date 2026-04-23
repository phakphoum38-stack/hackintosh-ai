from fastapi import APIRouter
from backend.core.security import create_token

router = APIRouter()

@router.post("/login")
def login(user: dict):

    token = create_token({
        "user_id": user["id"],
        "tenant_id": user["tenant_id"]
    })

    return {"access_token": token}
