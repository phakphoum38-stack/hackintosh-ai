# backend/api/build.py

from fastapi import APIRouter
from builder.efi_builder import build_efi

router = APIRouter()

@router.post("/build")
def build(config: dict):

    result = build_efi(config)

    return result
