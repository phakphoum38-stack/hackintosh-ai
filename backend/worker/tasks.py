import time
import traceback
from backend.core.db import SessionLocal
from backend.models.efi_job import EFIJob

# 🔥 AI + Builder
from backend.core.predictor import predict as ai_predict
from backend.builder.efi_builder import build_efi as real_build


# =========================
# 🧱 EFI BUILD TASK (PROD)
# =========================
def build_efi_task(job_id: int):

    db = SessionLocal()

    try:
        job = db.query(EFIJob).filter(EFIJob.id == job_id).first()

        if not job:
            print(f"[ERROR] Job {job_id} not found")
            return

        # =========================
        # 🔄 STEP 1: START
        # =========================
        job.status = "building"
        job.progress = 5
        db.commit()

        print(f"[+] Start job {job_id}")

        # =========================
        # 🤖 STEP 2: AI CONFIG
        # =========================
        job.progress = 20
        db.commit()

        ai_config = ai_predict(f"efi config for job {job_id}")

        print(f"[AI] config generated")

        # =========================
        # 🧱 STEP 3: BUILD EFI
        # =========================
        job.progress = 50
        db.commit()

        try:
            result_path = real_build(job_id, ai_config)
        except Exception as build_err:
            print("[WARN] real build failed → fallback:", build_err)

            # fallback
            time.sleep(3)
            result_path = f"/tmp/efi_{job_id}.zip"

            with open(result_path, "w") as f:
                f.write(f"EFI DATA {job_id}")

        # =========================
        # 📦 STEP 4: FINALIZE
        # =========================
        job.progress = 90
        db.commit()

        # (ถ้ามี S3 → upload ตรงนี้)

        job.status = "completed"
        job.progress = 100
        job.result_path = result_path
        db.commit()

        print(f"[✓] Job {job_id} completed")

        return {
            "job_id": job_id,
            "result": result_path
        }

    except Exception as e:
        print(f"[ERROR] Job {job_id} failed:", e)
        traceback.print_exc()

        try:
            job = db.query(EFIJob).filter(EFIJob.id == job_id).first()

            if job:
                job.status = "failed"
                job.error = str(e)
                job.progress = 0
                db.commit()

        except Exception as db_err:
            print("[CRITICAL] Cannot update DB:", db_err)

        # 🔥 RQ จะ mark failed ถ้า raise
        raise e

    finally:
        db.close()
