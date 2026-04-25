import os
import sys
import time
import logging
from redis import Redis
from rq import Worker, Queue
from rq.registry import FailedJobRegistry

# =========================
# 🔥 LOGGING
# =========================
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)

# =========================
# 🔥 ENV / REDIS
# =========================
REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379")
conn = Redis.from_url(REDIS_URL)

# =========================
# 🔥 QUEUE LIST
# =========================
listen = ["efi"]  # เพิ่ม "ai" ได้

# =========================
# 🤖 PRELOAD AI MODEL
# =========================
try:
    from backend.core.predictor import load_model
    load_model()
    logging.info("✅ AI model loaded")
except Exception as e:
    logging.warning(f"⚠️ AI preload failed: {e}")

# =========================
# 📊 QUEUE MONITOR
# =========================
def print_queue_status(queue):
    try:
        failed_registry = FailedJobRegistry(queue=queue)

        logging.info(
            f"📊 Queue={queue.name} | waiting={queue.count} | failed={len(failed_registry)}"
        )

        # แสดง failed jobs (debug)
        failed_jobs = failed_registry.get_job_ids()
        if failed_jobs:
            logging.warning(f"❌ Failed jobs: {failed_jobs}")

    except Exception as e:
        logging.warning(f"[MONITOR ERROR] {e}")


# =========================
# ❤️ WORKER HEALTH CHECK
# =========================
def heartbeat():
    logging.info("❤️ Worker alive")


# =========================
# 🚀 START WORKER LOOP
# =========================
if __name__ == "__main__":

    try:
        queues = [Queue(name, connection=conn) for name in listen]

        worker = Worker(
            queues,
            connection=conn,
            default_timeout=600  # 10 นาที
        )

        logging.info("🚀 Worker started...")

        while True:

            # ❤️ health
            heartbeat()

            # 📊 queue status
            for q in queues:
                print_queue_status(q)

            # 🔥 process jobs
            worker.work(
                burst=True,             # ทำ batch แล้ว loop ใหม่
                with_scheduler=True     # รองรับ retry/delay
            )

            time.sleep(5)  # loop ทุก 5 วิ

    except KeyboardInterrupt:
        logging.info("🛑 Worker stopped")
        sys.exit(0)

    except Exception as e:
        logging.error(f"[FATAL] Worker crashed: {e}")
        sys.exit(1)
