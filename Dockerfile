FROM python:3.10-slim AS builder

WORKDIR /install
COPY requirements.txt .
RUN pip install --upgrade pip \
    && pip install --prefix=/install/deps --no-cache-dir -r requirements.txt


FROM python:3.10-slim

WORKDIR /app

COPY --from=builder /install/deps /usr/local

# ✅ ใช้วิธีเดียวจบ
COPY . .

# folder จำเป็น
RUN mkdir -p /app/output /app/EFI

# tools
RUN apt-get update && apt-get install -y zip && rm -rf /var/lib/apt/lists/*

ENV PYTHONPATH=.
ENV APP_MODE=api

CMD ["sh", "-c", "\
if [ \"$APP_MODE\" = \"worker\" ]; then \
    echo '🚀 worker mode'; \
    python worker.py 2>/dev/null || python worker/worker.py; \
else \
    echo '🚀 api mode'; \
    uvicorn backend.main:app --host 0.0.0.0 --port 8000; \
fi"]
