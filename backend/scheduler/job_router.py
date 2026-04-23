from core.queue import push_job

def submit_job(config):
    push_job(config)
    return {"status": "queued"}
