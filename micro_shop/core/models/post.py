from typing import TYPE_CHECKING

from sqlalchemy import String, Text, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from micro_shop.core.models.base import Base
from micro_shop.core.models.mixins import UserRelationMixin
    

class Post(UserRelationMixin, Base):
    _user_back_populates = "posts"

    title: Mapped[str] = mapped_column(String(100), unique=False)
    body: Mapped[str] = mapped_column(
        Text,
        default="", # значение по умолчанию для SQL Alchemy
        server_default="", # значение по умолчанию в БД
    )

    def __str__(self):
        return f"{self.__class__.__name__}(id={self.id}, title={self.title}, user_id={self.user_id})"

    def __repr__(self):
        return str(self)
