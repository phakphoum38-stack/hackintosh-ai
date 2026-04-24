# 🧱 STAGE 1: build dependencies
FROM python:3.10-slim AS builder

WORKDIR /app

COPY requirements.txt .

RUN pip install --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

# 🧱 STAGE 2: runtime (เบามาก)
FROM python:3.10-slim

WORKDIR /app

# copy เฉพาะ dependency
COPY --from=builder /usr/local/lib/python3.10 /usr/local/lib/python3.10
COPY --from=builder /usr/local/bin /usr/local/bin

# copy code เฉพาะที่ใช้
COPY backend/ backend/

ENV PYTHONPATH=.

# 🚀 run FastAPI
CMD ["uvicorn", "backend.main:app", "--host", "0.0.0.0", "--port", "8000"]
