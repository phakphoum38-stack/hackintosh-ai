from fastapi import FastAPI

app = FastAPI()

from api.routes import router
app.include_router(router)
