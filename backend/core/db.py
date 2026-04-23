import psycopg2

def get_conn():
    return psycopg2.connect(
        dbname="hackintosh",
        user="postgres",
        password="postgres",
        host="localhost"
    )
