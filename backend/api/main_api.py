from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from backend.core.db import get_db
from backend.core.middleware import get_current_user

from backend.models.predict_log import PredictLog
from backend.models.efi_job import EFIJob
from pydantic import BaseModel

router = APIRouter()

# =========================
# 🤖 REQUEST SCHEMA
# =========================
class PredictRequest(BaseModel):
    input_text: str


# =========================
# 🚀 3) /predict + save DB
# =========================
@router.post("/predict")
def predict(req: PredictRequest, db: Session = Depends(get_db), user=Depends(get_current_user)):

    result_text = req.input_text[::-1]  # 🔥 AI demo

    log = PredictLog(
        user_id=user["user_id"],
        input_text=req.input_text,
        prediction=result_text
    )

    db.add(log)
    db.commit()

    return {
        "result": result_text
    }


# =========================
# 🚀 4) EFI BUILD
# =========================
@router.post("/efi/build")
def build_efi(db: Session = Depends(get_db), user=Depends(get_current_user)):

    job = EFIJob(
        user_id=user["user_id"],
        status="building"
    )

    db.add(job)
    db.commit()
    db.refresh(job)

    return {
        "job_id": job.id,
        "status": job.status
    }


# =========================
# 🚀 5) EFI STATUS
# =========================
@router.get("/efi/status/{job_id}")
def get_status(job_id: int, db: Session = Depends(get_db), user=Depends(get_current_user)):

    job = db.query(EFIJob).filter(
        EFIJob.id == job_id,
        EFIJob.user_id == user["user_id"]  # 🔐 ป้องกันข้าม user
    ).first()

    if not job:
        return {"error": "job not found"}

    return {
        "job_id": job.id,
        "status": job.status,
        "result": job.result_path
    }


# =========================
# 🚀 6) PREDICT HISTORY
# =========================
@router.get("/predict/history")
def history(db: Session = Depends(get_db), user=Depends(get_current_user)):

    logs = db.query(PredictLog).filter(
        PredictLog.user_id == user["user_id"]
    ).all()

    return [
        {
            "input": l.input_text,
            "prediction": l.prediction
        }
        for l in logs
    ]
