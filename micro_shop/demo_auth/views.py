import secrets
import uuid
from typing import Annotated, Any
from time import time

from fastapi import APIRouter, Depends, HTTPException, status, Header, Response, Cookie
from fastapi.security import HTTPBasic, HTTPBasicCredentials


router = APIRouter(prefix="/demo-auth", tags=["Demo Auth"])

security = HTTPBasic()

@router.get("/basic-auth/")
def demo_basic_auth_credentials(
    credentials: Annotated[HTTPBasicCredentials, Depends(security)],
):
    return {
        "message": "Hi!",
        "username": credentials.username,
        "password": credentials.password
    }


usernames_to_passwords = {
    "admin": "admin",
    "john": "password",
}


def get_auth_user_username(
    credentials: Annotated[HTTPBasicCredentials, Depends(security)],
):
    unathed_exc = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid username or password",
        headers={"WWW-Authenticate": "Basic"},
    )
    correct_password = usernames_to_passwords.get(credentials.username)

    if not correct_password:
        raise unathed_exc
    if not secrets.compare_digest(
        credentials.password.encode("utf-8"),
        correct_password.encode("utf-8"),
    ):
        raise unathed_exc

    return credentials.username


# базовая аутентификация
@router.get("/basic-auth-username/")
def demo_basic_auth_username(
    auth_username: str = Depends(get_auth_user_username)
):
    return {
        "message": f"Hi! {auth_username}",
        "username": auth_username,
    }


static_auth_token_to_username = {
    "b6da755e30a9b43d50265ef5536d2": "admin",
    "3490245b6d7afd72789ec29de07afafccfa": "john",
}


def get_username_by_static_auth_token(
    static_token: str = Header(alias="x-auth-token") # получаем этот параметр из заголовка с названием "x-auth-token"
) -> str:
    if username := static_auth_token_to_username.get(static_token):
        return username
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="token invalid",
    )


# аутентифакация по токену
@router.get("/some-http-header-auth/")
def demo_basic_auth_username(
    username: str = Depends(get_username_by_static_auth_token)
):
    return {
        "message": f"Hi! {username}",
        "username": username,
    }


#аутентификация по cookie
COOKIES: dict[str, dict[str, Any]] = {}
COOKIE_SESSION_ID_KEY = "web-app-session-id"


def generate_session_id() -> str:
    return uuid.uuid4().hex


def get_session_data(
    session_id: str = Cookie(alias=COOKIE_SESSION_ID_KEY), # вынимаем значение из браузера пользователя по ключу COOKIE_SESSION_ID_KEY
) -> dict:
    if session_id not in COOKIES:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="not authenticated",
        )
    return COOKIES[session_id]


@router.post("/login-cookie/")
def demo_auth_login_set_cookie(
    response: Response,
    username: str = Depends(get_username_by_static_auth_token)
):
    session_id = generate_session_id()
    COOKIES[session_id] = {
        "username": username,
        "login_at": int(time()),
    }
    response.set_cookie(COOKIE_SESSION_ID_KEY, session_id)
    return {"result": "ok"}


@router.get("/check-cookie/")
def demo_auth_check_cookie(
    user_session_data: dict = Depends(get_session_data),
):
    username = user_session_data["username"]
    return {
        "message": f"Hello, {username}",
        **user_session_data,
    }


@router.get("logout-cookie")
def demo_auth_check_cookie(
    response: Response,
    user_session_data: dict = Depends(get_session_data),
    session_id: str = Cookie(alias=COOKIE_SESSION_ID_KEY),
):
    COOKIES.pop(session_id)
    response.delete_cookie(COOKIE_SESSION_ID_KEY) # Удаление кук из браузера пользователя
    username = user_session_data["username"]
    return {
        "message": f"Bye, {username}!",
        **user_session_data
    }
