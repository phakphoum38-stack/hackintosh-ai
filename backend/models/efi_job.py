from sqlalchemy import Column, Integer, String
from backend.core.db import Base

class EFIJob(Base):
    __tablename__ = "efi_jobs"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer)
    status = Column(String, default="pending")
    result_path = Column(String, nullable=True)
