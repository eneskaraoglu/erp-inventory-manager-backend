from pydantic import BaseModel, Field, EmailStr
from typing import Optional
from datetime import datetime


class UserBase(BaseModel):
    """Base User schema - shared fields"""
    username: str = Field(..., min_length=3, max_length=50, description="Username (unique)")
    email: EmailStr = Field(..., description="User email address")
    full_name: Optional[str] = Field(None, max_length=100, description="Full name")
    is_active: bool = Field(True, description="Is user active")
    role: str = Field("user", max_length=20, description="User role (user, admin, manager)")


class UserCreate(BaseModel):
    """Schema for creating a new user"""
    username: str = Field(..., min_length=3, max_length=50)
    email: EmailStr
    password: str = Field(..., min_length=6, max_length=100, description="Password (min 6 chars)")
    full_name: Optional[str] = Field(None, max_length=100)
    role: str = Field("user", max_length=20)


class UserUpdate(BaseModel):
    """Schema for updating a user - all fields optional"""
    username: Optional[str] = Field(None, min_length=3, max_length=50)
    email: Optional[EmailStr] = None
    password: Optional[str] = Field(None, min_length=6, max_length=100)
    full_name: Optional[str] = Field(None, max_length=100)
    is_active: Optional[bool] = None
    role: Optional[str] = Field(None, max_length=20)


class User(UserBase):
    """User schema with ID - returned from API (password excluded)"""
    id: int = Field(..., description="User ID")
    created_at: datetime = Field(..., description="Account creation date")

    class Config:
        from_attributes = True
        json_schema_extra = {
            "example": {
                "id": 1,
                "username": "johndoe",
                "email": "john@example.com",
                "full_name": "John Doe",
                "is_active": True,
                "role": "user",
                "created_at": "2026-01-11T10:00:00"
            }
        }
