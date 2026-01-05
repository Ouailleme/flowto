"""User Pydantic schemas for API validation"""
from pydantic import BaseModel, EmailStr, Field, field_validator, ConfigDict
from uuid import UUID
from datetime import datetime
from typing import Optional
from app.models.user import LanguageEnum, CurrencyEnum, CountryEnum


class UserCreate(BaseModel):
    """Schema for creating a new user"""
    email: EmailStr
    password: str = Field(..., min_length=6, max_length=100)
    full_name: Optional[str] = Field(None, max_length=255)
    company_name: str = Field(..., min_length=1, max_length=255)
    company_size: Optional[str] = Field("1-10", max_length=50)
    industry: Optional[str] = Field(None, max_length=100)
    country: Optional[str] = Field("FR", max_length=10)
    language: Optional[str] = Field("fr", max_length=10)
    currency: Optional[str] = Field("EUR", max_length=10)
    timezone: Optional[str] = Field("Europe/Paris", max_length=50)
    
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "email": "user@example.com",
                "password": "SecurePassword123!",
                "full_name": "John Doe",
                "company_name": "My Company",
                "company_size": "1-10",
                "country": "FR",
                "language": "fr",
                "currency": "EUR"
            }
        }
    )


class UserUpdate(BaseModel):
    """Schema for updating user information"""
    email: Optional[EmailStr] = None
    company_name: Optional[str] = Field(None, min_length=1, max_length=255)
    company_size: Optional[str] = Field(None, pattern="^(1-10|10-50|50-200|200\\+)$")
    language: Optional[LanguageEnum] = None
    country: Optional[CountryEnum] = None
    currency: Optional[CurrencyEnum] = None
    timezone: Optional[str] = None
    locale: Optional[str] = None
    
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "company_name": "Updated Company Name",
                "language": "en",
                "currency": "USD"
            }
        }
    )


class UserRead(BaseModel):
    """Schema for reading user data (response)"""
    model_config = ConfigDict(from_attributes=True)
    
    id: UUID
    email: str
    full_name: Optional[str]
    is_active: bool
    is_verified: bool
    created_at: datetime
    updated_at: datetime


class UserInDB(UserRead):
    """Schema for user data in database (includes hashed_password)"""
    hashed_password: str


class PasswordChange(BaseModel):
    """Schema for changing password"""
    current_password: str
    new_password: str = Field(..., min_length=8, max_length=100)
    
    @field_validator("new_password")
    @classmethod
    def password_strength(cls, v: str) -> str:
        """Validate password strength"""
        if len(v) < 8:
            raise ValueError("Password must be at least 8 characters")
        if not any(c.isupper() for c in v):
            raise ValueError("Password must contain at least one uppercase letter")
        if not any(c.islower() for c in v):
            raise ValueError("Password must contain at least one lowercase letter")
        if not any(c.isdigit() for c in v):
            raise ValueError("Password must contain at least one digit")
        return v

