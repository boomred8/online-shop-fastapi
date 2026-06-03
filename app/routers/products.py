from fastapi import APIRouter, HTTPException, status
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError


from app.core.database import SessionDep
from app.models import Product
from app.schemas import ProductCreateSchema, ProductReadSchema, ProductUpdateSchema


product_router = APIRouter(
    prefix="/products",
    tags=["Products"]
)


@product_router.post(
    "/",
    response_model=ProductReadSchema,
    status_code=status.HTTP_201_CREATED
)
async def create_product(
    product_data: ProductCreateSchema,
    db: SessionDep
):
    product = Product(**product_data.model_dump())

    db.add(product)

    try:
        await db.commit()
        await db.refresh(product)
    except IntegrityError:
        await db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Product creation failed"
        )

    return product


@product_router.get(
    "/",
    response_model=list[ProductReadSchema]
)
async def get_products(db: SessionDep):
    result = await db.execute(select(Product))
    products = result.scalars().all()

    return products


@product_router.get(
    "/{product_id}",
    response_model=ProductReadSchema
)
async def get_product_by_id(
    product_id: int,
    db: SessionDep
):
    result = await db.execute(
        select(Product).where(Product.id == product_id)
    )

    product = result.scalar_one_or_none()

    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found"
        )

    return product


@product_router.patch(
    "/{product_id}",
    response_model=ProductReadSchema
)
async def update_product(
    product_id: int,
    product_data: ProductUpdateSchema,
    db: SessionDep
):
    result = await db.execute(
        select(Product).where(Product.id == product_id)
    )

    product = result.scalar_one_or_none()

    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found"
        )

    update_data = product_data.model_dump(exclude_unset=True)

    for key, value in update_data.items():
        setattr(product, key, value)

    await db.commit()
    await db.refresh(product)

    return product


@product_router.delete("/{product_id}")
async def delete_product(
    product_id: int,
    db: SessionDep
):
    result = await db.execute(
        select(Product).where(Product.id == product_id)
    )

    product = result.scalar_one_or_none()

    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found"
        )

    product.is_available = False

    await db.commit()

    return {
        "message": "Product marked as unavailable"
    }