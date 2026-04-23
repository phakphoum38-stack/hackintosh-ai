import redis
import json

r = redis.Redis(host="localhost", port=6379, decode_responses=True)

def push_job(config):

    r.lpush("jobs", json.dumps(config))
