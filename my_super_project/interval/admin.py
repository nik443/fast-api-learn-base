from sys import prefix

from fastapi import APIRouter


router = APIRouter()

@router.post("/")
async def update_admin():
    return {"message": "Admin getting saccessfully"}