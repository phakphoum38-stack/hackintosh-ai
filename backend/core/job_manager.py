import uuid
from typing import Dict

JOBS: Dict[str, dict] = {}

def create_job(data: dict):
    job_id = str(uuid.uuid4())

    JOBS[job_id] = {
        "id": job_id,
        "status": "queued",
        "progress": 0,
        "result": None,
        "data": data
    }

    return JOBS[job_id]


def get_job(job_id: str):
    return JOBS.get(job_id)


def update_job(job_id: str, **kwargs):
    if job_id in JOBS:
        JOBS[job_id].update(kwargs)
