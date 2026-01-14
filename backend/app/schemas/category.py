from pydantic import BaseModel, Field

class CategoryBase(BaseModel):
    name: str = Field(..., min_length=3, max_length=100, description="Название категории")
    slug: str = Field(..., min_length=3, max_length=100, description="URL-friendly category name")

class CategoryCreate(CategoryBase):
    pass

class CategoryResponse(CategoryBase):
    id: int = Field(..., description="Unique category udentifire")

    class Config:
        form_attributes = True
        # orm_mode = True

