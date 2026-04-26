from fastapi import FastAPI
from backend.api.routes import router  # หรือ path ที่ถูก

app = FastAPI()
app.include_router(router)

@app.get("/")
def root():
    return {"status": "ok"}
