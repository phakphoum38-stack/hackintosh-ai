from fastapi import FastAPI
from pydantic import BaseModel
import platform
import socket
import os

app = FastAPI(title="Hackintosh AI API")


# =========================
# MODELS
# =========================

class ScanResult(BaseModel):
    cpu: str
    hostname: str
    system: str


# =========================
# ROUTES
# =========================

@app.get("/")
def root():
    return {
        "status": "online",
        "project": "Hackintosh AI"
    }


@app.get("/health")
def health():
    return {
        "status": "healthy"
    }


@app.get("/system")
def system_info():
    return {
        "os": platform.system(),
        "release": platform.release(),
        "machine": platform.machine(),
        "processor": platform.processor()
    }


@app.get("/scan")
def scan_hardware():
    return {
        "cpu": platform.processor(),
        "hostname": socket.gethostname(),
        "system": platform.system()
    }


@app.post("/analyze")
def analyze(data: ScanResult):
    return {
        "compatible": True,
        "received": data.dict()
    }
