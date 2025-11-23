from fastapi import APIRouter
from src.api.handlers import read, write

router = APIRouter(tags=["key-value"])

@router.get("{key}")
async def get(key: str):
    return read(key)


@router.put("{key}")
async def put(key: str, value: str) -> int:
    return write(key, value)
