import os
from redis import Redis
from rq import Worker, Queue

redis_url = os.getenv("REDIS_URL")

if not redis_url:
    raise Exception("REDIS_URL not set")

conn = Redis.from_url(redis_url)

if __name__ == "__main__":
    queues = [Queue("efi", connection=conn)]

    worker = Worker(queues)

    print("🚀 Worker started...")
    worker.work()
