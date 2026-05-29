from fastapi import FastAPI
from pydantic import BaseModel
import platform
import socket
import os
import subprocess

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


# =========================
# CPU INFO
# =========================

@app.get("/cpu")
def cpu_info():

    return {
        "processor": platform.processor(),
        "cores": os.cpu_count()
    }


# =========================
# MEMORY INFO
# =========================

@app.get("/memory")
def memory_info():

    try:
        result = subprocess.check_output(
            "free -h",
            shell=True
        ).decode()

        return {
            "memory": result
        }

    except Exception as e:
        return {
            "error": str(e)
        }


# =========================
# DISK INFO
# =========================

@app.get("/disks")
def disk_info():

    try:
        result = subprocess.check_output(
            "lsblk -o NAME,SIZE,TYPE",
            shell=True
        ).decode()

        return {
            "disks": result
        }

    except Exception as e:
        return {
            "error": str(e)
        }
