from fastapi import FastAPI, Depends
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from sqlalchemy.orm import Session
import os
import uvicorn

# 🔐 DB + Auth
from backend.core.db import get_db
from backend.core.middleware import get_current_user
from backend.core.init_db import init_db

# 📦 Models
from backend.models.predict_log import PredictLog
from backend.models.efi_job import EFIJob

# 🔥 QUEUE + WORKER
from backend.core.queue import redis_conn
from rq import Queue, Retry
from rq.job import Job
from rq.registry import FailedJobRegistry
from backend.worker.tasks import build_efi_task

app = FastAPI()

# =========================
# 🔥 INIT DB
# =========================
init_db()

# =========================
# 🔥 QUEUE INIT
# =========================
queue = Queue("efi", connection=redis_conn)

# =========================
# 🤖 REQUEST SCHEMA
# =========================
class PredictRequest(BaseModel):
    input_text: str

# =========================
# 🤖 AI PREDICT + SAVE DB
# =========================
@app.post("/predict")
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
        "input": req.input_text,
        "prediction": result_text,
        "status": "success"
    }

# =========================
# 📊 PREDICT HISTORY
# =========================
@app.get("/predict/history")
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

# =========================
# 🧱 EFI BUILD (FIXED)
# =========================
@app.post("/efi/build")
def build_efi(
    db: Session = Depends(get_db),
    user=Depends(get_current_user)
):
    job = EFIJob(
        user_id=user["user_id"],
        status="queued",
        progress=0
    )

    db.add(job)
    db.commit()
    db.refresh(job)

    # 🔥 enqueue เข้า worker
    queue.enqueue(
        build_efi_task,
        job.id,
        retry=Retry(max=3, interval=[10, 30, 60])
    )

    return {
        "job_id": job.id,
        "status": "queued"
    }

# =========================
# 📊 EFI STATUS (UPGRADE)
# =========================
@app.get("/efi/status/{job_id}")
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
# 📥 DOWNLOAD (S3 URL)
# =========================
@app.get("/efi/download/{job_id}")
def download_efi(
    job_id: int,
    db: Session = Depends(get_db),
    user=Depends(get_current_user)
):
    job = db.query(EFIJob).filter(
        EFIJob.id == job_id,
        EFIJob.user_id == user["user_id"]
    ).first()

    if not job or not job.result_path:
        return {"error": "file not ready"}

    return {
        "download_url": job.result_path
    }

# =========================
# 🧪 DEBUG QUEUE
# =========================
@app.get("/debug/queue")
def debug_queue():
    q = Queue("efi", connection=redis_conn)
    failed_registry = FailedJobRegistry(queue=q)

    return {
        "waiting_jobs": q.count,
        "failed_jobs": failed_registry.get_job_ids()
    }

# =========================
# 🧪 DEBUG JOB
# =========================
@app.get("/debug/job/{job_id}")
def debug_job(job_id: str):
    try:
        job = Job.fetch(job_id, connection=redis_conn)

        return {
            "status": job.get_status(),
            "result": job.result,
            "error": job.exc_info
        }

    except Exception:
        return {"error": "job not found"}

# =========================
# 📊 STATUS
# =========================
@app.get("/status")
def status():
    return {
        "service": "ai-saas",
        "status": "running",
        "queue": "efi",
        "api_version": "3.0.0"
    }

# =========================
# ❤️ HEALTH
# =========================
@app.get("/health")
def health():
    return {"status": "ok"}

# =========================
# 🚀 ENTRY POINT
# =========================
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
