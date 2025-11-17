"""
Database Schemas

Define your MongoDB collection schemas here using Pydantic models.
These schemas are used for data validation in your application.

Each Pydantic model represents a collection in your database.
Model name is converted to lowercase for the collection name:
- User -> "user" collection
- Product -> "product" collection
- BlogPost -> "blogs" collection
"""

from pydantic import BaseModel, Field, field_validator
from typing import Optional, Literal

# Brand-specific schemas for Lady Salon Brașov

class Appointment(BaseModel):
    """
    Appointments collection schema
    Collection name: "appointment"
    """
    name: str = Field(..., description="Client full name", min_length=2, max_length=80)
    phone: str = Field(..., description="Client phone number", min_length=6, max_length=20)
    service: str = Field(..., description="Requested service")
    date: str = Field(..., description="Requested date (YYYY-MM-DD)")
    time: str = Field(..., description="Requested time (HH:MM)")
    notes: Optional[str] = Field(None, description="Optional message from client", max_length=500)
    status: Literal['pending','confirmed','cancelled'] = 'pending'

    @field_validator('date')
    @classmethod
    def validate_date(cls, v: str):
        # basic format check, more validation can be added in business logic
        if len(v.split('-')) != 3:
            raise ValueError('Date must be in format YYYY-MM-DD')
        return v

    @field_validator('time')
    @classmethod
    def validate_time(cls, v: str):
        if len(v.split(':')) != 2:
            raise ValueError('Time must be in format HH:MM')
        return v

class Review(BaseModel):
    """
    Client reviews
    Collection name: "review"
    """
    name: str = Field(..., description="Client name")
    text: str = Field(..., description="Review text", max_length=400)
    rating: int = Field(5, ge=1, le=5, description="Rating 1-5")
    avatar_url: Optional[str] = Field(None, description="Avatar image URL")

class GalleryItem(BaseModel):
    """
    Gallery items
    Collection name: "galleryitem" (used only if we decide to store gallery in DB)
    """
    title: str = Field(...)
    image_url: str = Field(...)
    category: Optional[str] = Field(None)

# Example schemas kept for reference
class User(BaseModel):
    name: str
    email: str
    address: str
    age: Optional[int] = None
    is_active: bool = True

class Product(BaseModel):
    title: str
    description: Optional[str] = None
    price: float
    category: str
    in_stock: bool = True
