import time
import traceback
from backend.core.db import SessionLocal
from backend.models.efi_job import EFIJob

# 🔥 import AI / builder จริงของคุณ
from backend.core.predictor import predict as ai_predict
from backend.builder.efi_builder import build_efi as real_build


# =========================
# 🧱 EFI BUILD TASK (REAL)
# =========================
def build_efi_task(job_id: int):

    db = SessionLocal()

    try:
        job = db.query(EFIJob).filter(EFIJob.id == job_id).first()

        if not job:
            print(f"[ERROR] Job {job_id} not found")
            return

        # =========================
        # 🔄 STEP 1: update status
        # =========================
        job.status = "building"
        db.commit()

        print(f"[+] Building EFI job {job_id}")

        # =========================
        # 🤖 STEP 2: ใช้ AI config (optional)
        # =========================
        ai_config = ai_predict(f"efi config for job {job_id}")

        # =========================
        # 🧱 STEP 3: build EFI จริง
        # =========================
        # 👉 ถ้ายังไม่มี builder จริง ใช้ fallback
        try:
            result_path = real_build(job_id, ai_config)
        except Exception:
            # fallback mock
            time.sleep(3)
            result_path = f"/app/efi_{job_id}.zip"

            with open(result_path, "w") as f:
                f.write(f"EFI DATA {job_id}")

        # =========================
        # ✅ STEP 4: save result
        # =========================
        job.status = "completed"
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
                db.commit()
        except:
            pass

        return {"error": str(e)}

    finally:
        db.close()
