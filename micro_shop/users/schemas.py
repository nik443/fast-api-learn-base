from pydantic import BaseModel, EmailStr, Field, ConfigDict


class CreateUser(BaseModel):
    username: str = Field(min_length=1, max_length=30)
    email: EmailStr


class UserSchema(BaseModel):
    model_config = ConfigDict(strict=True) # strict - строгоя проверка, по умолчанию pydantic пытается привести поле к необходимому типу

    username: str
    password: bytes
    email: EmailStr | None = None
    active: bool = True

