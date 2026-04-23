from backend.core.db import engine

def save_result(config, result):

    conn = engine.connect()

    conn.execute(
        "INSERT INTO jobs (tenant_id, status) VALUES (%s, %s)",
        (config["tenant_id"], result["success"])
    )
