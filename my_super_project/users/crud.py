from fastapi import APIRouter

from my_super_project.users.schemas import CreateUser


def create_user(user_in: CreateUser):
    user = user_in.model_dump()
    return {
        "success": True,
        "user": user,
    }
