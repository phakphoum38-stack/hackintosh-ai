import time
from backend.core.db import SessionLocal
from backend.models.efi_job import EFIJob

# =========================
# 🧱 EFI BUILD TASK
# =========================
def build_efi_task(job_id: int):

    db = SessionLocal()

    job = db.query(EFIJob).filter(EFIJob.id == job_id).first()

    if not job:
        return

    try:
        # 🔥 จำลอง build จริง
        job.status = "building"
        db.commit()

        time.sleep(5)  # simulate heavy work

        # 🔥 สมมติสร้างไฟล์
        result_path = f"/app/efi_{job_id}.zip"

        with open(result_path, "w") as f:
            f.write("EFI DATA")

        job.status = "completed"
        job.result_path = result_path
        db.commit()

    except Exception as e:
        job.status = "failed"
        db.commit()

    finally:
        db.close()
