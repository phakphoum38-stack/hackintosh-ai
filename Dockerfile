# =========================
# 🧱 STAGE 1: build deps
# =========================
FROM python:3.10-slim AS builder

WORKDIR /install

COPY requirements.txt .

RUN pip install --upgrade pip \
    && pip install --prefix=/install/deps --no-cache-dir -r requirements.txt


# =========================
# 🧱 STAGE 2: runtime
# =========================
FROM python:3.10-slim

WORKDIR /app

# copy python deps
COPY --from=builder /install/deps /usr/local

# copy source code
COPY backend/ backend/
COPY worker/ worker/  # ถ้ามี worker

# =========================
# 🧠 OPTIONAL EFI SUPPORT
# =========================
COPY . /tmp/build

RUN mkdir -p /app/EFI && \
    if [ -d "/tmp/build/EFI" ]; then \
        echo "✅ EFI found, copying..." && \
        cp -r /tmp/build/EFI/* /app/EFI/; \
    else \
        echo "⚠️ No EFI found, skipping"; \
    fi

# zip EFI ถ้ามี
RUN apt-get update && apt-get install -y zip && \
    cd /app && \
    if [ "$(ls -A EFI 2>/dev/null)" ]; then \
        zip -r efi.zip EFI; \
    else \
        echo "No EFI to zip"; \
    fi

ENV PYTHONPATH=.

# =========================
# 🔀 MODE SWITCH (API / WORKER)
# =========================
ENV APP_MODE=api

CMD ["sh", "-c", "\
if [ \"$APP_MODE\" = \"worker\" ]; then \
    python worker/worker.py; \
else \
    uvicorn backend.main:app --host 0.0.0.0 --port 8000; \
fi"]
