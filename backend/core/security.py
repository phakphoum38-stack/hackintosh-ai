import jwt
import datetime

SECRET_KEY = "change-this-secret"
ALGORITHM = "HS256"

# =========================
# 🔐 CREATE TOKEN
# =========================
def create_token(data: dict, expires_minutes: int = 60):
    payload = data.copy()
    payload["exp"] = datetime.datetime.utcnow() + datetime.timedelta(minutes=expires_minutes)

    token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)
    return token

# =========================
# 🔓 VERIFY TOKEN
# =========================
def verify_token(token: str):
    try:
        decoded = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return decoded
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None
