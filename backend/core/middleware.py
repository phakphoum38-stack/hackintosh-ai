from fastapi import Header, HTTPException, Depends
from backend.core.security import verify_token

# =========================
# 🔐 JWT AUTH MIDDLEWARE
# =========================
def get_current_user(authorization: str = Header(None)):

    if not authorization:
        raise HTTPException(status_code=401, detail="Missing Authorization header")

    try:
        scheme, token = authorization.split()

        if scheme.lower() != "bearer":
            raise HTTPException(status_code=401, detail="Invalid auth scheme")

    except:
        raise HTTPException(status_code=401, detail="Invalid Authorization format")

    payload = verify_token(token)

    if not payload:
        raise HTTPException(status_code=401, detail="Invalid or expired token")

    return payload


# =========================
# 👑 ROLE CHECK MIDDLEWARE
# =========================
def require_role(allowed_roles: list):

    def role_checker(user=Depends(get_current_user)):

        role = user.get("role")

        if role not in allowed_roles:
            raise HTTPException(
                status_code=403,
                detail=f"Access denied. Required roles: {allowed_roles}"
            )

        return user

    return role_checker
