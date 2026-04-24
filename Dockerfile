# 🧱 STAGE 1: build dependencies
FROM python:3.10-slim AS builder

WORKDIR /app

COPY requirements.txt .

RUN pip install --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

# 🧱 STAGE 2: runtime
FROM python:3.10-slim

WORKDIR /app

# copy dependency
COPY --from=builder /usr/local/lib/python3.10 /usr/local/lib/python3.10
COPY --from=builder /usr/local/bin /usr/local/bin

# copy code
COPY backend/ backend/

# ✅ รับ EFI จาก pipeline
ARG EFI_PATH=EFI
COPY ${EFI_PATH} /app/EFI

# กันพัง
RUN mkdir -p /app/EFI

# 📦 zip EFI อัตโนมัติ
RUN apt-get update && apt-get install -y zip \
    && cd /app && zip -r efi.zip EFI || true

ENV PYTHONPATH=.

# debug
RUN echo "📦 EFI inside container:" && ls -la /app/EFI || true

# 🚀 run API
CMD ["uvicorn", "backend.main:app", "--host", "0.0.0.0", "--port", "8000"]
