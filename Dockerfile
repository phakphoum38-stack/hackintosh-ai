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

# copy ทั้ง repo (กันพลาดเรื่องไฟล์หาย)
COPY . /tmp/build

# =========================
# 📦 COPY CODE (safe mode)
# =========================
RUN cp -r /tmp/build/backend /app/backend

# copy worker ถ้ามี
RUN if [ -d "/tmp/build/worker" ]; then \
        echo "✅ worker folder found"; \
        cp -r /tmp/build/worker /app/worker; \
    else \
        echo "⚠️ no worker folder"; \
    fi

# copy worker.py ถ้ามี
RUN if [ -f "/tmp/build/worker.py" ]; then \
        echo "✅ worker.py found"; \
        cp /tmp/build/worker.py /app/worker.py; \
    fi

# =========================
# 🧠 OPTIONAL EFI
# =========================
RUN mkdir -p /app/EFI && \
    if [ -d "/tmp/build/EFI" ]; then \
        echo "✅ EFI found"; \
        cp -r /tmp/build/EFI/* /app/EFI/; \
    else \
        echo "⚠️ No EFI found"; \
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
# 🔀 MODE SWITCH
# =========================
ENV APP_MODE=api

CMD ["sh", "-c", "\
if [ \"$APP_MODE\" = \"worker\" ]; then \
    echo '🚀 running worker'; \
    python worker.py || python worker/worker.py; \
else \
    echo '🚀 running API'; \
    uvicorn backend.main:app --host 0.0.0.0 --port 8000; \
fi"]
