import redis
import json
import time
import traceback

from backend.core.db import SessionLocal
from backend.models.efi_job import EFIJob

r = redis.Redis(host="redis", port=6379, decode_responses=True)

QUEUE_NAME = "vm_jobs"


# =========================
# 🖥️ MOCK QEMU RUN
# =========================
def run_qemu(config):
    time.sleep(2)  # simulate boot
    return {
        "success": 1,
        "log": "boot success"
    }


# =========================
# 🔄 WORKER LOOP
# =========================
def loop():

    print("🚀 Worker started...")

    while True:
        try:
            job_data = r.brpop(QUEUE_NAME)

            _, raw = job_data
            payload = json.loads(raw)

            job_id = payload.get("job_id")
            config = payload.get("config", {})

            db = SessionLocal()

            job = db.query(EFIJob).filter(EFIJob.id == job_id).first()

            if not job:
                print(f"[ERROR] Job {job_id} not found")
                continue

            # =========================
            # 🔥 STEP 1: START
            # =========================
            job.status = "building"
            job.progress = 10
            db.commit()

            print(f"[+] Start job {job_id}")

            # =========================
            # 🤖 STEP 2: AI (mock)
            # =========================
            time.sleep(1)
            job.progress = 40
            db.commit()

            # =========================
            # 🧱 STEP 3: BUILD / QEMU
            # =========================
            result = run_qemu(config)

            job.progress = 80
            db.commit()

            # =========================
            # 📦 STEP 4: SAVE RESULT
            # =========================
            result_path = f"/app/efi_{job_id}.zip"

            with open(result_path, "w") as f:
                f.write(json.dumps(result))

            # =========================
            # ✅ DONE
            # =========================
            job.status = "completed"
            job.progress = 100
            job.result_path = result_path
            db.commit()

            print(f"[✓] Job {job_id} completed")

        except Exception as e:
            print("[ERROR]", e)
            traceback.print_exc()

            try:
                if job:
                    job.status = "failed"
                    job.error = str(e)
                    db.commit()
            except:
                pass

        finally:
            try:
                db.close()
            except:
                pass
