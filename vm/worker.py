import redis
import json

r = redis.Redis()

def run_vm(config):

    return {
        "log": "boot success",
        "success": 1
    }


def loop():

    while True:

        job = r.brpop("vm_jobs")

        _, raw = job
        config = json.loads(raw)

        result = run_vm(config)

        r.lpush("vm_results", json.dumps(result))
