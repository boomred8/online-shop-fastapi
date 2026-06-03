from pydantic import BaseModel, Field, ConfigDict
from typing import Annotated, Optional
from datetime import datetime


class OrderItemCreateSchema(BaseModel):
    product_id: Annotated[int, Field(..., gt=0, description="Product ID")]
    quantity: Annotated[int, Field(default=1, ge=1, description="Product quantity")]


class OrderCreateSchema(BaseModel):
    customer_name: Annotated[str, Field(..., min_length=2, max_length=255, description="Customer name")]
    phone_number: Annotated[str, Field(..., min_length=5, max_length=50, description="Customer phone number")]
    items: Annotated[list[OrderItemCreateSchema], Field(..., min_length=1, description="Order items")]


class OrderItemReadSchema(BaseModel):
    id: int = Field(description="Order item ID")
    product_id: int = Field(description="Product ID")
    quantity: int = Field(description="Product quantity")

    model_config = ConfigDict(from_attributes=True)


class OrderReadSchema(BaseModel):
    id: int = Field(description="Order ID")
    customer_name: str = Field(description="Customer name")
    phone_number: str = Field(description="Customer phone number")
    created_at: datetime = Field(description="Order created date")
    items: list[OrderItemReadSchema] = Field(description="Order items")

    model_config = ConfigDict(from_attributes=True)