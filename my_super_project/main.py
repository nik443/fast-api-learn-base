from typing import Annotated

import uvicorn
from fastapi import FastAPI, Path
from pydantic import EmailStr, BaseModel

app = FastAPI()


class CreateUser(BaseModel):
    email: EmailStr


@app.post("/users/{user_id}/")
async def create_user(user_id: Annotated[int, Path(ge=0, le=1_000_000)]): # валидация через аннотацию типов
    return {
        "message": "success",
        "user_id": user_id,
    }


if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)
