from fastapi import APIRouter, Depends, Form, HTTPException, status
from fastapi.security import HTTPBearer
from pydantic import BaseModel

from micro_shop.demo_auth.helpers import (
    create_access_token,
    create_refresh_token,
)
from micro_shop.demo_auth.validations import users_db, get_current_token_payload, get_current_auth_user, \
    get_current_auth_user_for_refresh
from micro_shop.users.schemas import UserSchema
from micro_shop.auth import utils as auth_utils


http_bearer = HTTPBearer(auto_error=False)

class TokenInfo(BaseModel):
    access_token: str
    refresh_token: str | None = None
    token_type: str = "Bearer"


router = APIRouter(
    prefix="/jwt",
    tags=["JWT"],
    dependencies=[Depends(http_bearer)],
)


def validate_auth_user(
    username: str = Form(),
    password: str = Form(),
):
    unathed_exc = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="invalid username or password"
    )
    if not (user := users_db.get(username)):
        raise unathed_exc

    if not auth_utils.validate_password(password=password, hashed_password=user.password):
        raise unathed_exc

    if not user.active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="user inactive",
        )

    return user


def get_current_active_auth_user(
    user: UserSchema = Depends(get_current_auth_user)
):
    if user.active:
        return user
    raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail="user inactive",
    )



@router.post("/login", response_model=TokenInfo)
def auth_user_issue_jwt(
    user: UserSchema = Depends(validate_auth_user)
):
    token = create_access_token(user)
    refresh_token = create_refresh_token(user)
    return TokenInfo(
        access_token=token,
        refresh_token=refresh_token
    )


@router.post(
    "/refresh",
    response_model=TokenInfo,
)
def auth_refresh_jwt(
    user: UserSchema = Depends(get_current_auth_user_for_refresh),
):
    access_token = create_access_token(user)
    return TokenInfo(access_token=access_token)



@router.get("/users/me/")
def auth_user_check_self_info(
    user: UserSchema = Depends(get_current_active_auth_user),
    payload: dict = Depends(get_current_token_payload),
):
    iat = payload.get("iat")
    return {
        "username": user.username,
        "email": user.email,
        "logged_in_at": iat,
    }
