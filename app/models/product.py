from pydantic import BaseModel, Field
from typing import Optional


class ProductBase(BaseModel):
    """Base Product schema - shared fields"""
    name: str = Field(..., min_length=1, max_length=100, description="Product name")
    description: Optional[str] = Field(None, max_length=500, description="Product description")
    price: float = Field(..., gt=0, description="Product price (must be positive)")
    stock: int = Field(..., ge=0, description="Stock quantity (must be non-negative)")
    category: Optional[str] = Field(None, max_length=50, description="Product category")


class ProductCreate(ProductBase):
    """Schema for creating a new product"""
    pass


class ProductUpdate(BaseModel):
    """Schema for updating a product - all fields optional"""
    name: Optional[str] = Field(None, min_length=1, max_length=100)
    description: Optional[str] = Field(None, max_length=500)
    price: Optional[float] = Field(None, gt=0)
    stock: Optional[int] = Field(None, ge=0)
    category: Optional[str] = Field(None, max_length=50)


class Product(ProductBase):
    """Product schema with ID - returned from API"""
    id: int = Field(..., description="Product ID")

    class Config:
        from_attributes = True
        json_schema_extra = {
            "example": {
                "id": 1,
                "name": "Laptop",
                "description": "High-performance laptop",
                "price": 999.99,
                "stock": 50,
                "category": "Electronics"
            }
        }
