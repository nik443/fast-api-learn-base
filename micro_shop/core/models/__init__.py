# Здесь обязательно нужно указать модели таблиц, с которыми должен работать alembic

__all__ = (
    "Base",
    "Product",
    "Post",
    "User",
    "Profile",
    "Order",
    "DatabaseHelper",
    "OrderProductAssociation",
    "db_helper",
)

from micro_shop.core.models.base import Base
from micro_shop.core.models.product import Product
from micro_shop.core.models.user import User
from micro_shop.core.models.post import Post
from micro_shop.core.models.profile import Profile
from micro_shop.core.models.order import Order
from micro_shop.core.models.order_product_association import OrderProductAssociation
from micro_shop.core.models.db_helper import DatabaseHelper, db_helper