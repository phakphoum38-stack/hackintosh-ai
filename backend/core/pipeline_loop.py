import json
import redis
from backend.core.log_analyzer import analyze
from backend.core.ai_feedback_loop import update_learning_pipeline

r = redis.Redis(host="localhost", port=6379, decode_responses=True)


def pipeline_loop():

    while True:

        job = r.brpop("vm_results", timeout=10)

        if not job:
            continue

        _, raw = job
        data = json.loads(raw)

        # 🧠 analyze result
        analyze(data)

        # 🔁 update learning dataset
        update_learning_pipeline()

        print("Pipeline updated")
