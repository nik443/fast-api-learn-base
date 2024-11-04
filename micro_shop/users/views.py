from fastapi import APIRouter

from micro_shop.users.schemas import CreateUser
from micro_shop.users import crud


router = APIRouter(prefix="/users", tags=["users"])

@router.post("/users/")
def create_user(user: CreateUser):
    return crud.create_user(user_in=user)
