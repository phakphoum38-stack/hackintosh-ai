import threading
import time
from backend.core.job_manager import JOBS
from backend.builder.pipeline import run_pipeline

def worker_loop():
    while True:
        for job_id, job in JOBS.items():
            if job["status"] == "queued":
                job["status"] = "running"

                threading.Thread(
                    target=run_pipeline,
                    args=(job_id, job["data"]),
                    daemon=True
                ).start()

        time.sleep(1)
