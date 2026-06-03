from fastapi import FastAPI, APIRouter
from fastapi.staticfiles import StaticFiles
import uvicorn

from starlette.middleware.sessions import SessionMiddleware

from app.core.config import secret_key
from app.routers import *


app = FastAPI(title="Online Shop")

app.mount("/static", StaticFiles(directory="static"), name="static")

app.add_middleware(
    SessionMiddleware,
    secret_key=secret_key
)

api_router = APIRouter(prefix="/api/v1")

api_router.include_router(product_router)
api_router.include_router(order_router)
api_router.include_router(cart_router)

app.include_router(page_router)
app.include_router(api_router)


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)