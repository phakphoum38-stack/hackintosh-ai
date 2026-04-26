from fastapi import APIRouter
from backend.core.job_manager import create_job, get_job

router = APIRouter()

@router.post("/build")
def build(spec: dict):
    job = create_job(spec)
    return {"job_id": job["id"]}


@router.get("/job/{job_id}")
def job_status(job_id: str):
    job = get_job(job_id)

    if not job:
        return {"error": "not found"}

    return job


@router.get("/download/{job_id}")
def download(job_id: str):
    job = get_job(job_id)

    if not job or job["status"] != "done":
        return {"error": "not ready"}

    return {
        "download": job["result"]
    }
