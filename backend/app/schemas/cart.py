from pydantic import BaseModel, Field
from typing import Optional, List


class CartItemBase(BaseModel):
    product_id: int = Field(..., description="Product ID")
    quantity: int = Field(..., description="Quantity")

class CartItemCreate(CartItemBase):
    pass

class CartItemUpdate(BaseModel):
    product_id: int = Field(..., description="Product ID")
    quantity: int = Field(..., gt=0, description="New Quantity")

class CartItem(BaseModel):
     product_id: int
     name: str = Field(..., description="Product Name")
     price: float = Field(..., gt=0, description="Price")
     quantity: int = Field(..., gt=0, description="Quantity in cart")
     subtotal: float = Field(..., gt=0, description="Total price for this item")
     image_url: Optional[str] = Field(None, description="Product Image URL")


class CartResponse(BaseModel):
    items: List[CartItem] = Field(..., description="List of item in cart")
    total: float = Field(..., description="Total cart price")
    items_count: int = Field(..., description="Total number of items in cart")