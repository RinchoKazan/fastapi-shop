from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional, List
from .category import CategoryResponse


class ProductBase(BaseModel):
    name: str = Field(..., min_length=3, max_length=200, description="product name")
    description: Optional[str] = Field(None, description="product description")
    price: float = Field(..., gt=0, description="product price")
    category_id: int = Field(..., description="product category id")
    image_url: Optional[str] = Field(None, description="product image URL")

class ProductCreate(ProductBase):
    pass

class ProductResponse(BaseModel):
    id: int = Field(..., description="Unique product ID")
    name: str
    description: Optional[str]
    price: float
    category_id: int
    image_url: Optional[str]
    created_at: datetime
    category: CategoryResponse = Field(..., description="product category details")

    class Config:
        form_attributes = True


class ProductListResponse(BaseModel):
    products: List[ProductResponse]
    total: int = Field(..., description="total number of products")