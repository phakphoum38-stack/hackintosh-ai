from fastapi import APIRouter, Request

router = APIRouter()

@router.post("/webhook")
async def webhook(req: Request):

    event = await req.json()

    if event["type"] == "invoice.paid":
        print("Upgrade tenant plan")

    return {"status": "ok"}
