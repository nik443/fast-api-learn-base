from contextlib import asynccontextmanager

from fastapi import FastAPI
from pydantic import BaseModel, EmailStr
import uvicorn
from sqlalchemy.ext.asyncio import AsyncSession

from micro_shop.core.config import setting
from core.models import Base
from item_views import router as items_router
from micro_shop.core.models import db_helper, User
from users.views import router as users_router
from api_v1 import router as router_v1


@asynccontextmanager
async def lifespan(app: FastAPI):

    yield


app = FastAPI(lifespan=lifespan)
app.include_router(items_router)
app.include_router(users_router)
app.include_router(router=router_v1, prefix=setting.api_v1_prefix)


@app.get("/")
def hello_index():
    return {
        "message": "Hello index!",
    }


@app.get("/hello/")
def hello(name: str = "World"):
    name = name.strip().title()
    return {"message": f"Hello {name}!"}


@app.get("/calc/add/")
def add(a: int, b: int):
    return {
        "a": a,
        "b": b,
        "result": a + b,
    }


if __name__ == '__main__':
    uvicorn.run("main:app", reload=True)