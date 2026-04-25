import os
import redis
import json
import uuid

# =========================
# 🔥 REDIS CONNECT (PROD READY)
# =========================
REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379")

r = redis.from_url(REDIS_URL, decode_responses=True)

QUEUE_NAME = "vm_jobs"


# =========================
# 🚀 PUSH JOB
# =========================
def push_job(data: dict):

    job_id = str(uuid.uuid4())

    job = {
        "id": job_id,
        "status": "queued",
        "data": data
    }

    # push เข้า queue
    r.lpush(QUEUE_NAME, json.dumps(job))

    # save job status แยก (สำคัญ)
    r.set(f"job:{job_id}", json.dumps(job))

    return job_id


# =========================
# 🔥 GET JOB (WORKER)
# =========================
def get_job():

    _, job_data = r.brpop(QUEUE_NAME)
    job = json.loads(job_data)

    return job


# =========================
# 📊 UPDATE JOB STATUS
# =========================
def update_job(job_id: str, status: str, result: str = None):

    job_key = f"job:{job_id}"

    job_data = r.get(job_key)

    if not job_data:
        return

    job = json.loads(job_data)

    job["status"] = status
    job["result"] = result

    r.set(job_key, json.dumps(job))


# =========================
# 📊 GET JOB STATUS
# =========================
def get_job_status(job_id: str):

    job_data = r.get(f"job:{job_id}")

    if not job_data:
        return None

    return json.loads(job_data)
