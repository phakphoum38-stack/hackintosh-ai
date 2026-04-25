from sqlalchemy import Column, Integer, String, Text
from backend.core.db import Base

class PredictLog(Base):
    __tablename__ = "predict_logs"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer)
    input_text = Column(Text)
    prediction = Column(Text)
