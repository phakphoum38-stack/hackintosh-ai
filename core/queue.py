import os
import redis
import json
import uuid
import time

# =========================
# 🔥 REDIS CONNECT (PROD READY)
# =========================
REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379")

r = redis.from_url(
    REDIS_URL,
    decode_responses=True,
    socket_timeout=5,
    retry_on_timeout=True
)

QUEUE_NAME = "vm_jobs"


# =========================
# 🚀 PUSH JOB
# =========================
def push_job(data: dict):

    job_id = str(uuid.uuid4())

    job = {
        "id": job_id,
        "status": "queued",
        "progress": 0,
        "data": data,
        "created_at": time.time()
    }

    # push เข้า queue
    r.lpush(QUEUE_NAME, json.dumps(job))

    # save job status แยก
    r.set(f"job:{job_id}", json.dumps(job))

    return job_id


# =========================
# 🔥 GET JOB (WORKER)
# =========================
def get_job():

    try:
        _, job_data = r.brpop(QUEUE_NAME)
        return json.loads(job_data)

    except Exception as e:
        print(f"[QUEUE ERROR] {e}")
        return None


# =========================
# 📊 UPDATE JOB STATUS
# =========================
def update_job(
    job_id: str,
    status: str,
    result: str = None,
    progress: int = None,
    error: str = None
):

    job_key = f"job:{job_id}"
    job_data = r.get(job_key)

    if not job_data:
        return

    job = json.loads(job_data)

    job["status"] = status

    if progress is not None:
        job["progress"] = progress

    if result is not None:
        job["result"] = result

    if error is not None:
        job["error"] = error

    job["updated_at"] = time.time()

    r.set(job_key, json.dumps(job))


# =========================
# 📊 GET JOB STATUS
# =========================
def get_job_status(job_id: str):

    job_data = r.get(f"job:{job_id}")

    if not job_data:
        return None

    return json.loads(job_data)


# =========================
# 🧪 DEBUG QUEUE
# =========================
def get_queue_size():
    return r.llen(QUEUE_NAME)


def ping():
    try:
        return r.ping()
    except Exception:
        return False
