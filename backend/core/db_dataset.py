# backend/core/db_dataset.py

from backend.core.db import get_conn

def fetch_logs():

    conn = get_conn()
    cur = conn.cursor()

    cur.execute("SELECT cpu, gpu, success FROM boot_logs")

    return cur.fetchall()
