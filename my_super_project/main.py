from fastapi import FastAPI, Depends, status

from dependencies import get_token_header, get_query_token
from interval import admin
from routers import items, users


app = FastAPI()

app.include_router(users.router)
app.include_router(items.router)
app.include_router(
    admin.router,
    prefix="/admin",
    tags=["admin"],
    dependencies=[Depends(get_token_header)],
    responses={status.HTTP_418_IM_A_TEAPOT: {"description": "I'm teapot"}},
)


@app.get("/")
async def root():
    return {"message": "Hello Bigger Applications!"}
