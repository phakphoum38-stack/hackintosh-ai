from fastapi import FastAPI, Depends, HTTPException
from fastapi.responses import JSONResponse, FileResponse, RedirectResponse
from pydantic import BaseModel
from sqlalchemy.orm import Session
import os
import uvicorn
import threading

# 🔐 DB + Auth
from backend.core.db import get_db
from backend.core.middleware import get_current_user
from backend.core.init_db import init_db

# 🔐 AUTH ROUTER
from backend.auth.routes import router as auth_router

# 📦 Models
from backend.models.predict_log import PredictLog
from backend.models.efi_job import EFIJob

# 🔥 task
from backend.worker.tasks import build_efi_task

# =========================
# 🔥 REDIS MODE SWITCH
# =========================
REDIS_URL = os.getenv("REDIS_URL")
USE_QUEUE = bool(REDIS_URL)

queue = None
redis_conn = None

if USE_QUEUE:
    try:
        print("🚀 Running in QUEUE MODE")

        from redis import Redis
        from rq import Queue

        redis_conn = Redis.from_url(REDIS_URL)
        queue = Queue("efi", connection=redis_conn)

    except Exception as e:
        print("❌ Redis error → fallback FREE MODE:", e)
        USE_QUEUE = False
else:
    print("⚠️ Running in FREE MODE (no Redis)")

# =========================
# 🚀 APP INIT
# =========================
app = FastAPI()

@app.on_event("startup")
def startup():
    print("🔥 App starting...")
    init_db()

@app.on_event("shutdown")
def shutdown():
    print("🛑 App shutting down...")

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
# 🧱 EFI BUILD
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
    # 🚀 QUEUE MODE
    # =========================
    if USE_QUEUE and queue:
        queue.enqueue(build_efi_task, job.id)

        return {
            "job_id": job.id,
            "status": "queued",
            "mode": "queue"
        }

    # =========================
    # 🚀 FREE MODE (THREAD)
    # =========================
    def run_job():
        try:
            build_efi_task(job.id)
        except Exception as e:
            db_job = db.query(EFIJob).get(job.id)
            db_job.status = "failed"
            db_job.error = str(e)
            db.commit()

    threading.Thread(target=run_job, daemon=True).start()

    return {
        "job_id": job.id,
        "status": "running",
        "mode": "thread"
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
        raise HTTPException(404, "job not found")

    return {
        "job_id": job.id,
        "status": job.status,
        "progress": job.progress,
        "result": job.result_path,
        "error": job.error
    }

# =========================
# 📥 DOWNLOAD (FIXED)
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
        raise HTTPException(404, "file not ready")

    if not os.path.exists(job.result_path):
        raise HTTPException(404, "file missing")

    return FileResponse(
        job.result_path,
        filename="EFI.zip",
        media_type="application/zip"
    )

# =========================
# ❤️ HEALTH
# =========================
@app.get("/health")
def health():
    return {
        "status": "ok",
        "mode": "queue" if USE_QUEUE else "free"
    }

# =========================
# 🚀 ENTRY POINT
# =========================
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
