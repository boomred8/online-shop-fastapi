from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates
from fastapi import HTTPException
from fastapi import Form
from fastapi.responses import HTMLResponse, RedirectResponse

from sqlalchemy.orm import selectinload
from sqlalchemy import select


from app.models import Product, Order, OrderItem
from app.models import Product
from app.core.database import SessionDep

page_router = APIRouter(tags=["Pages"])

templates = Jinja2Templates(directory="templates")


@page_router.get("/", response_class=HTMLResponse)
async def home_page(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="index.html",
    )

@page_router.get("/products", response_class=HTMLResponse)
async def products_page(
    request: Request,
    db: SessionDep
):
    result = await db.execute(select(Product))
    products = result.scalars().all()

    return templates.TemplateResponse(
        request=request,
        name="products.html",
        context={
            "products": products
        }
    )

@page_router.get("/products/{product_id}", response_class=HTMLResponse)
async def product_detail_page(
    product_id: int,
    request: Request,
    db: SessionDep
):
    result = await db.execute(
        select(Product).where(
            Product.id == product_id
        )
    )

    product = result.scalar_one_or_none()

    if not product:
        raise HTTPException(
            status_code=404,
            detail="Product not found"
        )

    return templates.TemplateResponse(
        request=request,
        name="product_detail.html",
        context={
            "product": product
        }
    )

@page_router.get("/cart", response_class=HTMLResponse)
async def cart_page(
    request: Request,
    db: SessionDep
):
    cart = request.session.get("cart", {})

    if not cart:
        return templates.TemplateResponse(
            request=request,
            name="cart.html",
            context={
                "items": [],
                "total": 0
            }
        )

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
            "product": product,
            "quantity": quantity,
            "subtotal": subtotal
        })

    return templates.TemplateResponse(
        request=request,
        name="cart.html",
        context={
            "items": items,
            "total": total
        }
    )

@page_router.get("/checkout", response_class=HTMLResponse)
async def checkout_page(
    request: Request
):
    cart = request.session.get("cart", {})

    if not cart:
        return RedirectResponse(
            url="/cart",
            status_code=303
        )

    return templates.TemplateResponse(
        request=request,
        name="checkout.html",
        context={}
    )

@page_router.post("/checkout")
async def checkout_submit(
    request: Request,
    customer_name: str = Form(...),
    phone_number: str = Form(...),
    db: SessionDep = None
):
    cart = request.session.get("cart", {})

    if not cart:
        raise HTTPException(
            status_code=400,
            detail="Cart is empty"
        )

    order = Order(
        customer_name=customer_name,
        phone_number=phone_number
    )

    db.add(order)

    await db.flush()

    for product_id, quantity in cart.items():

        order_item = OrderItem(
            order_id=order.id,
            product_id=int(product_id),
            quantity=quantity
        )

        db.add(order_item)

    await db.commit()

    request.session["cart"] = {}

    return RedirectResponse(
        url="/success",
        status_code=303
    )

@page_router.get("/success", response_class=HTMLResponse)
async def success_page(
    request: Request
):
    return templates.TemplateResponse(
        request=request,
        name="success.html",
        context={}
    )

@page_router.get("/orders", response_class=HTMLResponse)
async def orders_page(
    request: Request,
    db: SessionDep
):
    result = await db.execute(
        select(Order).options(
            selectinload(Order.items).selectinload(OrderItem.product)
        )
    )

    orders = result.scalars().all()

    return templates.TemplateResponse(
        request=request,
        name="orders.html",
        context={
            "orders": orders
        }
    )