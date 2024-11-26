from typing import TYPE_CHECKING
from sqlalchemy.orm import Mapped, relationship

from micro_shop.core.models.base import Base


if TYPE_CHECKING:
    from micro_shop.core.models.order_product_association import OrderProductAssociation
    from micro_shop.core.models.order import Order


class Product(Base):
    name: Mapped[str]
    description: Mapped[str]
    price: Mapped[int]

    orders_details: Mapped[list["OrderProductAssociation"]] = relationship(back_populates="product")
