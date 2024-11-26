from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import func
from sqlalchemy.orm import Mapped, relationship
from sqlalchemy.testing.schema import mapped_column

from micro_shop.core.models.base import Base


if TYPE_CHECKING:
    from micro_shop.core.models.order_product_association import OrderProductAssociation

class Order(Base):
    promocode: Mapped[str | None]
    created_ad: Mapped[datetime] = mapped_column(
        server_default=func.now(), # использует sql функцию NOW для datetime на стороне сервера (дает значение по умолчанию силами БД, при создании записи)
        default=datetime.now, # использует datetime.now на стороне sqlalchemy (дает значение по умолчанию силами питона и после передает в БД значение)
    )

    products_details: Mapped[list["OrderProductAssociation"]] = relationship(back_populates="order")
