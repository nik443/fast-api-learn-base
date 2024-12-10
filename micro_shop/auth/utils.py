from datetime import timedelta, datetime, timezone

import bcrypt
import jwt

from micro_shop.core.config import setting


def encode_jwt(
    payload: dict,
    private_key: str = setting.auth_jwt.private_key_path.read_text(),
    algorithm: str = setting.auth_jwt.algorithm,
    expire_minutes: int = setting.auth_jwt.access_token_expire_minutes,
    expire_timedelta: timedelta | None = None
):
    to_encode = payload.copy()
    now = datetime.now(tz=timezone.utc)
    to_encode.update(
        exp=now + expire_timedelta if expire_timedelta else now + timedelta(minutes=expire_minutes),
        iat=now
    )
    encoded = jwt.encode(
        to_encode,
        private_key,
        algorithm,
    )
    return encoded


def decode_jwt(
    token: str | bytes,
    public_key: str = setting.auth_jwt.public_key_path.read_text(),
    algorithm: str = setting.auth_jwt.algorithm,
) -> dict:
    decoded = jwt.decode(
        token,
        public_key,
        algorithms=[algorithm],
    )
    return decoded


def hash_password(password: str) -> bytes:
    salt = bcrypt.gensalt()
    password_bytes: bytes = password.encode()
    return bcrypt.hashpw(password_bytes, salt)


def validate_password(password: str, hashed_password: bytes) -> bool:
    return bcrypt.checkpw(
        password=password.encode(),
        hashed_password=hashed_password,
    )
