from datetime import datetime, timedelta
import jwt

SECRET = "SECRET_KEY"

def create_token(data: dict):

    payload = data.copy()
    payload["exp"] = datetime.utcnow() + timedelta(days=1)

    return jwt.encode(payload, SECRET, algorithm="HS256")


def decode_token(token: str):

    return jwt.decode(token, SECRET, algorithms=["HS256"])
