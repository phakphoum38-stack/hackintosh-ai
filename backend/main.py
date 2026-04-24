from fastapi import FastAPI
from fastapi.responses import FileResponse, JSONResponse
import os
import uvicorn

app = FastAPI()

# =========================
# 🔥 โหลด EFI แบบ zip
# =========================
@app.get("/efi")
def download_efi():
    path = "/app/efi.zip"
    if os.path.exists(path):
        return FileResponse(
            path,
            filename="EFI.zip",
            media_type="application/zip"
        )
    return JSONResponse(
        status_code=404,
        content={"error": "EFI not found"}
    )

# =========================
# 🔥 ดูไฟล์ใน EFI
# =========================
@app.get("/efi/list")
def list_efi():
    base = "/app/EFI"
    if not os.path.exists(base):
        return JSONResponse(
            status_code=404,
            content={"error": "EFI not found"}
        )

    try:
        return {
            "files": os.listdir(base)
        }
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={"error": str(e)}
        )

# =========================
# 🔥 health check (K8s)
# =========================
@app.get("/health")
def health():
    return {
        "status": "ok",
        "service": "ai-saas",
        "efi_exists": os.path.exists("/app/EFI"),
        "zip_exists": os.path.exists("/app/efi.zip")
    }

# =========================
# 🚀 ENTRY POINT (IMPORTANT)
# =========================
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
