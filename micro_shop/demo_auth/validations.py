from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jwt import InvalidTokenError
from starlette import status

from micro_shop.auth import utils as auth_utils
from micro_shop.demo_auth.helpers import TOKEN_TYPE_FIELD, ACCESS_TOKEN_TYPE, REFRESH_TOKEN_TYPE
from micro_shop.users.schemas import UserSchema

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/jwt/login") # здесь указываем откуда будем пытаться получить Bearer-токен, в нашем случае в роутере jwt/login


john = UserSchema(
    username="john",
    password=auth_utils.hash_password("qwerty"),
    email="john@example.com",
    active=True,
)
sam = UserSchema(
    username="sam",
    password=auth_utils.hash_password("secret"),
    active=True,
)
users_db: dict[str, UserSchema] = {
    john.username: john,
    sam.username: sam,
}


def validate_token_type(payload: dict, token_type: str) -> bool:
    current_token_type = payload.get(TOKEN_TYPE_FIELD)
    if current_token_type == token_type:
        return True
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail=f"Incorrect token type: get {current_token_type}, expected {token_type}"
    )


def get_user_by_token_sub(payload: dict) -> UserSchema:
    username: str | None = payload.get("sub")
    if user := users_db.get(username):
        return user
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="user not found",
    )



def get_current_token_payload(
    token: str = Depends(oauth2_scheme),
) -> UserSchema:
    try:
        payload = auth_utils.decode_jwt(token)
    except InvalidTokenError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"invalid token error: {e}",
        )
    return payload


def get_current_auth_user(
    payload: dict = Depends(get_current_token_payload),
) -> UserSchema:
    validate_token_type(payload=payload, token_type=ACCESS_TOKEN_TYPE)
    return get_user_by_token_sub(payload)


def get_current_auth_user_for_refresh(
    payload: dict = Depends(get_current_token_payload),
) -> UserSchema:
    validate_token_type(payload=payload, token_type=REFRESH_TOKEN_TYPE)
    return get_user_by_token_sub(payload)

