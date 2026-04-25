import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# =========================
# 🔥 DATABASE URL (PRODUCTION SAFE)
# =========================
DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "sqlite:///./test.db"  # fallback local
)

# =========================
# ENGINE
# =========================
engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True
)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

Base = declarative_base()

# =========================
# DB DEPENDENCY
# =========================
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
