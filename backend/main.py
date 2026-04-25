from fastapi import FastAPI, Depends
from fastapi.responses import FileResponse, JSONResponse
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

app = FastAPI()

# =========================
# 🔥 INIT DB
# =========================
init_db()

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
    result_text = req.input_text[::-1]  # 🔥 AI demo

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
        "result": job.result_path
    }

# =========================
# 📦 DOWNLOAD EFI ZIP
# =========================
@app.get("/efi")
def download_efi():
    path = "/app/efi.zip"
    if os.path.exists(path):
        return FileResponse(
            path,
            filename="EFI.zip",
            media_type="application/zip"
        )
    return JSONResponse(
        status_code=404,
        content={"error": "EFI not found"}
    )

# =========================
# 📂 LIST EFI FILES
# =========================
@app.get("/efi/list")
def list_efi():
    base = "/app/EFI"
    if not os.path.exists(base):
        return JSONResponse(
            status_code=404,
            content={"error": "EFI not found"}
        )

    try:
        return {"files": os.listdir(base)}
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={"error": str(e)}
        )

# =========================
# 📊 STATUS
# =========================
@app.get("/status")
def status():
    return {
        "service": "ai-saas",
        "status": "running",
        "efi_exists": os.path.exists("/app/EFI"),
        "zip_exists": os.path.exists("/app/efi.zip"),
        "api_version": "2.0.0"
    }

# =========================
# ❤️ HEALTH
# =========================
@app.get("/health")
def health():
    return {
        "status": "ok",
        "service": "ai-saas"
    }

# =========================
# 🚀 ENTRY POINT
# =========================
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
