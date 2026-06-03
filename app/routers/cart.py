from fastapi import APIRouter, Request, HTTPException, status
from fastapi.responses import RedirectResponse
from sqlalchemy import select

from app.core.database import SessionDep
from app.models import Product


cart_router = APIRouter(
    prefix="/cart",
    tags=["Cart"]
)


@cart_router.post("/add/{product_id}")
async def add_to_cart(
    product_id: int,
    request: Request,
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

    if not product.is_available:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Product is out of stock"
        )

    cart = request.session.get("cart", {})

    product_id_str = str(product_id)

    if product_id_str in cart:
        cart[product_id_str] += 1
    else:
        cart[product_id_str] = 1

    request.session["cart"] = cart

    return RedirectResponse(
        url="/cart",
        status_code=303
    )


@cart_router.get("/")
async def get_cart(
    request: Request,
    db: SessionDep
):
    cart = request.session.get("cart", {})

    if not cart:
        return {
            "items": [],
            "total": 0
        }

    product_ids = [int(product_id) for product_id in cart.keys()]

    result = await db.execute(
        select(Product).where(Product.id.in_(product_ids))
    )

    products = result.scalars().all()

    items = []
    total = 0

    for product in products:
        quantity = cart[str(product.id)]
        subtotal = float(product.price) * quantity
        total += subtotal

        items.append({
            "product_id": product.id,
            "name": product.name,
            "price": float(product.price),
            "quantity": quantity,
            "subtotal": subtotal
        })

    return {
        "items": items,
        "total": total
    }

@cart_router.post("/remove/{product_id}")
async def remove_from_cart(
    product_id: int,
    request: Request
):
    cart = request.session.get("cart", {})

    product_id_str = str(product_id)

    if product_id_str not in cart:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found in cart"
        )

    del cart[product_id_str]

    request.session["cart"] = cart

    return RedirectResponse(
        url="/cart",
        status_code=303
    )

@cart_router.post("/increase/{product_id}")
async def increase_quantity(
    product_id: int,
    request: Request
):
    cart = request.session.get("cart", {})

    product_id_str = str(product_id)

    if product_id_str in cart:
        cart[product_id_str] += 1

    request.session["cart"] = cart

    return RedirectResponse(
        url="/cart",
        status_code=303
    )


@cart_router.post("/decrease/{product_id}")
async def decrease_quantity(
    product_id: int,
    request: Request
):
    cart = request.session.get("cart", {})

    product_id_str = str(product_id)

    if product_id_str in cart:
        cart[product_id_str] -= 1

        if cart[product_id_str] <= 0:
            del cart[product_id_str]

    request.session["cart"] = cart

    return RedirectResponse(
        url="/cart",
        status_code=303
    )