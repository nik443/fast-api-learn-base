from fastapi import APIRouter

from my_super_project.users.schemas import CreateUser
from my_super_project.users import crud


router = APIRouter(
    prefix="/users",
    tags=["users"],
)

@router.post("/")
def create_user(user: CreateUser):
    return crud.create_user(user)