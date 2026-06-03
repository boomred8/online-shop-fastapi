from fastapi import APIRouter, HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import selectinload

from app.core.database import SessionDep
from app.models import Product, Order, OrderItem
from app.schemas import OrderCreateSchema, OrderReadSchema


order_router = APIRouter(
    prefix="/orders",
    tags=["Orders"]
)


@order_router.post(
    "/",
    response_model=OrderReadSchema,
    status_code=status.HTTP_201_CREATED
)
async def create_order(
    order_data: OrderCreateSchema,
    db: SessionDep
):
    order = Order(
        customer_name=order_data.customer_name,
        phone_number=order_data.phone_number
    )

    db.add(order)
    await db.flush()

    for item in order_data.items:
        result = await db.execute(
            select(Product).where(Product.id == item.product_id)
        )

        product = result.scalar_one_or_none()

        if not product:
            await db.rollback()
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Product with id {item.product_id} not found"
            )

        order_item = OrderItem(
            order_id=order.id,
            product_id=item.product_id,
            quantity=item.quantity
        )

        db.add(order_item)

    await db.commit()

    result = await db.execute(
        select(Order)
        .options(selectinload(Order.items))
        .where(Order.id == order.id)
    )

    return result.scalar_one()


@order_router.get(
    "/",
    response_model=list[OrderReadSchema]
)
async def get_orders(db: SessionDep):
    result = await db.execute(
        select(Order).options(selectinload(Order.items))
    )

    orders = result.scalars().all()

    return orders


@order_router.get(
    "/{order_id}",
    response_model=OrderReadSchema
)
async def get_order_by_id(
    order_id: int,
    db: SessionDep
):
    result = await db.execute(
        select(Order)
        .options(selectinload(Order.items))
        .where(Order.id == order_id)
    )

    order = result.scalar_one_or_none()

    if not order:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Order not found"
        )

    return order