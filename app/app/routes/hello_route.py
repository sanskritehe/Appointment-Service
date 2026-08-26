from fastapi import APIRouter
from app.services.hello_service import get_hello_message

router = APIRouter()

@router.get("/hello")
async def hello():
    return get_hello_message()
