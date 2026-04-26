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

# =========================
# 📦 COPY CODE (ตรงไปตรงมา)
# =========================
COPY backend/ backend/

# worker optional (ไม่พังถ้าไม่มีไฟล์นี้)
COPY worker.py ./ 2>/dev/null || true
COPY worker/ worker/ 2>/dev/null || true

# =========================
# 🧠 OPTIONAL EFI
# =========================
RUN mkdir -p /app/EFI

# (ไม่ใช้ COPY EFI ตรง ๆ แล้ว → กัน build fail)
# ถ้ามีจริงค่อย mount หรือ inject ตอน runtime

# =========================
# 📦 SYSTEM TOOLS
# =========================
RUN apt-get update && apt-get install -y zip && rm -rf /var/lib/apt/lists/*

# =========================
# 📂 OUTPUT DIR (Phase 2)
# =========================
RUN mkdir -p /app/output

ENV PYTHONPATH=.

# =========================
# 🔀 MODE SWITCH
# =========================
ENV APP_MODE=api

CMD ["sh", "-c", "\
if [ \"$APP_MODE\" = \"worker\" ]; then \
    echo '🚀 running worker'; \
    python worker.py 2>/dev/null || python worker/worker.py; \
else \
    echo '🚀 running API'; \
    uvicorn backend.main:app --host 0.0.0.0 --port 8000; \
fi"]
