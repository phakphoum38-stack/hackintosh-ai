from fastapi import FastAPI
from backend.scheduler.job_router import submit_job

app = FastAPI()

@app.post("/build")
def build(config: dict):
    return submit_job(config)
