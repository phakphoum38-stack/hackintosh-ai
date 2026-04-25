from fastapi import FastAPI, Depends
from fastapi.responses import JSONResponse, FileResponse, RedirectResponse
from pydantic import BaseModel
from sqlalchemy.orm import Session
import os
import uvicorn

# 🔐 DB + Auth
from backend.core.db import get_db
from backend.core.middleware import get_current_user
from backend.core.init_db import init_db

# 🔐 AUTH ROUTER
from backend.auth.routes import router as auth_router

# 📦 Models
from backend.models.predict_log import PredictLog
from backend.models.efi_job import EFIJob

# =========================
# 🔥 REDIS MODE SWITCH
# =========================
REDIS_URL = os.getenv("REDIS_URL")
USE_QUEUE = bool(REDIS_URL)

if USE_QUEUE:
    print("🚀 Running in QUEUE MODE")
    from redis import Redis
    from rq import Queue, Retry
    from rq.registry import FailedJobRegistry

    redis_conn = Redis.from_url(REDIS_URL)
    queue = Queue("efi", connection=redis_conn)
else:
    print("⚠️ Running in FREE MODE (no Redis)")

# 🔥 import task (ใช้ได้ทั้ง 2 mode)
from backend.worker.tasks import build_efi_task

# =========================
# 🚀 APP INIT
# =========================
app = FastAPI()

init_db()
app.include_router(auth_router)

# =========================
# 🤖 REQUEST SCHEMA
# =========================
class PredictRequest(BaseModel):
    input_text: str

# =========================
# 🔄 ROOT → LOGIN
# =========================
@app.get("/")
def root():
    return RedirectResponse(url="/login")

# =========================
# 🔐 LOGIN PAGE
# =========================
@app.get("/login")
def login_page():
    return FileResponse("login.html")

# =========================
# 🖥️ DASHBOARD PAGE
# =========================
@app.get("/dashboard")
def dashboard_page():
    return FileResponse("dashboard.html")

# =========================
# 🤖 AI PREDICT
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
# 🧱 EFI BUILD (AUTO MODE)
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

    # =========================
    # 🚀 QUEUE MODE (PRO)
    # =========================
    if USE_QUEUE:
        queue.enqueue(
            build_efi_task,
            job.id
        )

        return {
            "job_id": job.id,
            "status": "queued",
            "mode": "queue"
        }

    # =========================
    # 🚀 FREE MODE (SYNC)
    # =========================
    else:
        build_efi_task(job.id)

        return {
            "job_id": job.id,
            "status": "completed",
            "mode": "sync"
        }

# =========================
# 📊 EFI STATUS
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
# 📊 EFI HISTORY
# =========================
@app.get("/efi/history")
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
# 📥 DOWNLOAD
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
# 🧪 DEBUG QUEUE (SAFE)
# =========================
@app.get("/debug/queue")
def debug_queue():
    if not USE_QUEUE:
        return {"mode": "free", "message": "queue disabled"}

    from rq.registry import FailedJobRegistry

    q = queue
    failed_registry = FailedJobRegistry(queue=q)

    return {
        "waiting_jobs": q.count,
        "failed_jobs": failed_registry.get_job_ids()
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
