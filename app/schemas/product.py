from pydantic import BaseModel, Field, ConfigDict
from typing import Annotated, Optional
from decimal import Decimal


class ProductCreateSchema(BaseModel):
    name: Annotated[str, Field(..., min_length=2, max_length=255, description="Product name")]
    description: Annotated[Optional[str], Field(None, description="Product description")]
    price: Annotated[Decimal, Field(..., gt=0, description="Product price")]
    image: Annotated[Optional[str], Field(None, max_length=500, description="Product image URL")]
    is_available: Annotated[bool, Field(default=True, description="Is product available")]


class ProductReadSchema(BaseModel):
    id: int = Field(description="Product ID")
    name: str = Field(description="Product name")
    description: Optional[str] = Field(description="Product description")
    price: Decimal = Field(description="Product price")
    image: Optional[str] = Field(description="Product image URL")
    is_available: bool = Field(description="Is product available")

    model_config = ConfigDict(from_attributes=True)


class ProductUpdateSchema(BaseModel):
    name: Annotated[Optional[str], Field(None, min_length=2, max_length=255, description="New product name")]
    description: Annotated[Optional[str], Field(None, description="New product description")]
    price: Annotated[Optional[Decimal], Field(None, gt=0, description="New product price")]
    image: Annotated[Optional[str], Field(None, max_length=500, description="New product image URL")]
    is_available: Annotated[Optional[bool], Field(None, description="New availability status")]

    model_config = ConfigDict(extra="forbid")