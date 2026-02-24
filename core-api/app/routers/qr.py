from fastapi import APIRouter

router = APIRouter()

@router.post("/generate")
async def generate_qr():
    return {"message": "QR generation - TODO Day 2"}

@router.get("/validate/{token}")
async def validate_qr(token: str):
    return {"message": "QR validation - TODO Day 2", "token": token}
