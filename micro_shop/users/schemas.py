from pydantic import BaseModel, EmailStr, Field


class CreateUser(BaseModel):
    username: str = Field(min_length=1, max_length=30)
    email: EmailStr