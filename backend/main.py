from fastapi import FastAPI, Header, HTTPException
from fastapi.responses import FileResponse, JSONResponse
from pydantic import BaseModel
import os
import uvicorn

app = FastAPI()

# =========================
# 🔐 SIMPLE API KEY (AUTH)
# =========================
API_KEY = "change-this-key"

def verify_key(x_api_key: str = Header(None)):
    if x_api_key != API_KEY:
        raise HTTPException(status_code=401, detail="Invalid API Key")

# =========================
# 🤖 AI PREDICT ENDPOINT
# =========================
class PredictRequest(BaseModel):
    input_text: str

@app.post("/predict")
def predict(req: PredictRequest, x_api_key: str = Header(None)):
    verify_key(x_api_key)

    # 🔥 ใส่ AI logic ตรงนี้
    result = {
        "input": req.input_text,
        "prediction": req.input_text[::-1],  # demo AI (reverse string)
        "confidence": 0.99,
        "status": "success"
    }

    return result

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
        return {"files": os.listdir(base)}
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={"error": str(e)}
        )

# =========================
# 📊 STATUS / DEBUG DASHBOARD
# =========================
@app.get("/status")
def status():
    return {
        "service": "ai-saas",
        "status": "running",
        "efi_exists": os.path.exists("/app/EFI"),
        "zip_exists": os.path.exists("/app/efi.zip"),
        "api_version": "1.0.0"
    }

# =========================
# 🔥 HEALTH CHECK
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
# 🚀 ENTRY POINT
# =========================
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
