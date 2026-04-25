from fastapi import HTTPException

# =========================
# 🔐 ROLE CHECKER
# =========================
def require_role(user: dict, allowed_roles: list):

    role = user.get("role")

    if role not in allowed_roles:
        raise HTTPException(
            status_code=403,
            detail=f"Access denied. Required roles: {allowed_roles}"
        )

    return True
