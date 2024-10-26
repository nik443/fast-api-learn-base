from typing import Annotated

import uvicorn
from fastapi import FastAPI, Path
from pydantic import EmailStr, BaseModel

from items_views import router as items_router
from users.views import router as user_router

app = FastAPI()
app.include_router(items_router)
app.include_router(user_router)


if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)
