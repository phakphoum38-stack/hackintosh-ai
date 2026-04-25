from fastapi import Header, HTTPException
from backend.core.security import verify_token

# =========================
# 🔐 JWT AUTH MIDDLEWARE
# =========================
def get_current_user(authorization: str = Header(None)):
    
    if not authorization:
        raise HTTPException(status_code=401, detail="Missing token")

    try:
        scheme, token = authorization.split()
        if scheme.lower() != "bearer":
            raise HTTPException(status_code=401, detail="Invalid auth scheme")
    except:
        raise HTTPException(status_code=401, detail="Invalid authorization header")

    payload = verify_token(token)

    if not payload:
        raise HTTPException(status_code=401, detail="Invalid or expired token")

    return payload
