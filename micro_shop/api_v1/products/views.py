from fastapi import APIRouter, HTTPException, status
from fastapi.params import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from micro_shop.api_v1.products import crud
from micro_shop.api_v1.products.schemas import ProductCreate, Product, ProductUpdate, ProductUpdatePartial
from micro_shop.api_v1.products.dependencies import product_by_id
from micro_shop.core.models.db_helper import db_helper

router = APIRouter(tags=["Products"])


@router.get("/", response_model=list[Product])
async def get_products(session: AsyncSession = Depends(db_helper.scoped_session_dependency)):
    return await crud.get_products(session=session)


@router.post(
    path="/",
    response_model=Product,
    status_code=status.HTTP_201_CREATED,
)
async def create_product(
    product_id: ProductCreate,
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
):
    return await crud.create_product(session, product_id)


@router.get("/{product_id}/")
async def get_product(
    product: Product = Depends(product_by_id),
):
    return product


@router.patch("/{product_id}/")
async def update_product(
    product_update: ProductUpdatePartial,
    product: Product = Depends(product_by_id),
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
):
    return await crud.update_product(
        session=session,
        product=product,
        product_update=product_update,
    )


@router.delete(path="/{product_id}/", status_code=status.HTTP_204_NO_CONTENT)
async def delete_product(
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
    product: Product = Depends(product_by_id),
) -> None:
    await crud.delete_product(session, product)