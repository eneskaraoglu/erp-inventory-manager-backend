from pydantic import BaseModel, Field, EmailStr
from typing import Optional


class CustomerBase(BaseModel):
    """Base Customer schema - shared fields"""
    name: str = Field(..., min_length=1, max_length=100, description="Customer name")
    email: EmailStr = Field(..., description="Customer email address")
    phone: Optional[str] = Field(None, max_length=20, description="Customer phone number")
    address: Optional[str] = Field(None, max_length=200, description="Customer address")
    company: Optional[str] = Field(None, max_length=100, description="Customer company")


class CustomerCreate(CustomerBase):
    """Schema for creating a new customer"""
    pass


class CustomerUpdate(BaseModel):
    """Schema for updating a customer - all fields optional"""
    name: Optional[str] = Field(None, min_length=1, max_length=100)
    email: Optional[EmailStr] = None
    phone: Optional[str] = Field(None, max_length=20)
    address: Optional[str] = Field(None, max_length=200)
    company: Optional[str] = Field(None, max_length=100)


class Customer(CustomerBase):
    """Customer schema with ID - returned from API"""
    id: int = Field(..., description="Customer ID")

    class Config:
        from_attributes = True
        json_schema_extra = {
            "example": {
                "id": 1,
                "name": "John Doe",
                "email": "john@example.com",
                "phone": "+1234567890",
                "address": "123 Main St, New York, NY",
                "company": "Acme Corp"
            }
        }
