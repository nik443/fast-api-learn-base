from sqlalchemy.orm import Mapped

from micro_shop.core.models.base import Base


class Product(Base):
    name: Mapped[str]
    description: Mapped[str]
    price: Mapped[int]
