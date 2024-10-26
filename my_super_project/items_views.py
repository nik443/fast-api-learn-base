from typing import Annotated

from fastapi import APIRouter, Path


router = APIRouter(
    prefix="/items",
    tags=["items"]
)


@router.get("/")
def list_items():
    return ["Item1", "Item2", "Item3"]


@router.get("/latest")
def get_last_item():
    return {
        "item": {"id": "0", "name": "latest"}
    }


@router.post("/{user_id}/")
async def create_user(user_id: Annotated[int, Path(ge=0, le=1_000_000)]): # валидация через аннотацию типов
    return {
        "message": "success",
        "user_id": user_id,
    }
