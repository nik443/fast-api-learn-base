from pydantic import BaseModel, Field, EmailStr


class CreateUser(BaseModel):
    username: str = Field(min_length=3, max_length=30)
    email: EmailStr