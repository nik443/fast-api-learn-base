from typing import TYPE_CHECKING

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from micro_shop.core.models.base import Base


if TYPE_CHECKING: # эту штука нужна для того, чтобы избежать циклического импорта (в user мы импортируем post)
    from micro_shop.core.models.post import Post
    from micro_shop.core.models.profile import Profile

class User(Base):
    username: Mapped[str] = mapped_column(String(32), unique=True)
    posts: Mapped[list["Post"]] = relationship(back_populates="user") # т.к. отношение один-ко-многим, то list["Post"]]
    profile: Mapped["Profile"] = relationship(back_populates="user")

    def __str__(self):
        return f"{self.__class__.__name__}(id={self.id}, username={self.username})"

    def __repr__(self):
        return str(self)