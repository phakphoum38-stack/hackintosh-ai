import traceback
import time
from backend.core.db import SessionLocal
from backend.models.efi_job import EFIJob

from backend.core.predictor import predict
from backend.builder.efi_builder import build_efi
from backend.core.storage import upload_file


def build_efi_task(job_id: int):

    db = SessionLocal()
    job = None

    try:
        job = db.query(EFIJob).filter(EFIJob.id == job_id).first()

        if not job:
            print(f"[ERROR] Job {job_id} not found")
            return

        # =========================
        # 🚀 START
        # =========================
        job.status = "building"
        job.progress = 10
        db.commit()

        print(f"[+] Job {job_id} started")

        # =========================
        # 🤖 AI CONFIG
        # =========================
        ai_config = predict(f"efi config {job_id}")

        job.progress = 40
        db.commit()

        # =========================
        # 🧱 BUILD EFI
        # =========================
        zip_path = build_efi(job_id, ai_config)

        job.progress = 80
        db.commit()

        # =========================
        # ☁️ UPLOAD S3
        # =========================
        key = f"efi/{job_id}.zip"
        url = upload_file(zip_path, key)

        # =========================
        # ✅ DONE
        # =========================
        job.status = "completed"
        job.progress = 100
        job.result_path = url
        db.commit()

        print(f"[✓] Job {job_id} completed")

        return url

    except Exception as e:
        print(f"[ERROR] Job {job_id} failed:", e)
        traceback.print_exc()

        if job:
            job.status = "failed"
            job.error = str(e)
            db.commit()

    finally:
        db.close()
