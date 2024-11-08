from typing import Annotated

from fastapi import Depends, Path, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from micro_shop.api_v1.products import crud
from micro_shop.api_v1.products.schemas import Product
from micro_shop.core.models import db_helper


async def product_by_id(
    product_id: Annotated[int, Path],
    session: AsyncSession = Depends(db_helper.scoped_session_dependency)
) -> Product:
    product_db = await crud.get_product(session, product_id)
    if product_db:
        return product_db
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Prodoct with id {product_id} not fount")