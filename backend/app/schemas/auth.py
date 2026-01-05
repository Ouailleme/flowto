"""Authentication schemas for login, registration, and token management."""
from pydantic import BaseModel, EmailStr, Field


class LoginRequest(BaseModel):
    """Login request schema."""
    email: EmailStr
    password: str = Field(..., min_length=6)


class TokenResponse(BaseModel):
    """Token response schema."""
    access_token: str
    refresh_token: str
    token_type: str = "bearer"


class UserResponse(BaseModel):
    """User response after login/registration."""
    id: str
    email: str
    full_name: str | None = None
    is_active: bool
    is_verified: bool


class LoginResponse(BaseModel):
    """Complete login response with user and tokens."""
    user: UserResponse
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
