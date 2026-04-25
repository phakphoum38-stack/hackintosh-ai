import os
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from redis import Redis
from rq import Queue, Retry
from pydantic import BaseModel

from backend.core.db import get_db
from backend.core.middleware import get_current_user

from backend.models.predict_log import PredictLog
from backend.models.efi_job import EFIJob

from backend.worker.tasks import build_efi_task

router = APIRouter()

# =========================
# 🔥 QUEUE INIT (สำคัญ)
# =========================
redis_conn = Redis.from_url(os.getenv("REDIS_URL"))
queue = Queue("efi", connection=redis_conn)

# =========================
# 🤖 REQUEST SCHEMA
# =========================
class PredictRequest(BaseModel):
    input_text: str


# =========================
# 🤖 /predict + save DB
# =========================
@router.post("/predict")
def predict(
    req: PredictRequest,
    db: Session = Depends(get_db),
    user=Depends(get_current_user)
):

    result_text = req.input_text[::-1]

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
# 🚀 EFI BUILD (RQ VERSION)
# =========================
@router.post("/efi/build")
def build_efi(
    db: Session = Depends(get_db),
    user=Depends(get_current_user)
):

    # 🔥 create job
    job = EFIJob(
        user_id=user["user_id"],
        status="queued",
        progress=0
    )

    db.add(job)
    db.commit()
    db.refresh(job)

    # 🔥 enqueue เข้า worker
    rq_job = queue.enqueue(
        build_efi_task,
        job.id,
        retry=Retry(max=3, interval=[10, 30, 60])
    )

    return {
        "job_id": job.id,
        "rq_job_id": rq_job.id,
        "status": "queued"
    }


# =========================
# 📊 EFI STATUS (UPGRADE)
# =========================
@router.get("/efi/status/{job_id}")
def get_status(
    job_id: int,
    db: Session = Depends(get_db),
    user=Depends(get_current_user)
):

    job = db.query(EFIJob).filter(
        EFIJob.id == job_id,
        EFIJob.user_id == user["user_id"]
    ).first()

    if not job:
        return {"error": "job not found"}

    return {
        "job_id": job.id,
        "status": job.status,
        "progress": job.progress,
        "result": job.result_path,
        "error": job.error
    }


# =========================
# 📊 EFI HISTORY (เพิ่มใหม่)
# =========================
@router.get("/efi/history")
def efi_history(
    db: Session = Depends(get_db),
    user=Depends(get_current_user)
):

    jobs = db.query(EFIJob).filter(
        EFIJob.user_id == user["user_id"]
    ).order_by(EFIJob.id.desc()).all()

    return [
        {
            "job_id": j.id,
            "status": j.status,
            "progress": j.progress,
            "result": j.result_path,
            "error": j.error
        }
        for j in jobs
    ]


# =========================
# 📊 PREDICT HISTORY
# =========================
@router.get("/predict/history")
def history(
    db: Session = Depends(get_db),
    user=Depends(get_current_user)
):

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
