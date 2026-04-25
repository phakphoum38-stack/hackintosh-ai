from backend.core.db import Base, engine

# import models ให้ครบ (สำคัญมาก ไม่งั้น table ไม่ถูกสร้าง)
from backend.models.user import User
from backend.models.predict_log import PredictLog
from backend.models.efi_job import EFIJob

def init_db():
    Base.metadata.create_all(bind=engine)
