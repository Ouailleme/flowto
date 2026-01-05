"""Authentication API endpoints"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.api.deps import get_current_user
from app.schemas.user import UserCreate, UserRead, PasswordChange
from app.schemas.auth import Token, LoginRequest
from app.services.auth_service import AuthService
from app.models.user import User

router = APIRouter(prefix="/auth", tags=["authentication"])


@router.post(
    "/register",
    response_model=UserRead,
    status_code=status.HTTP_201_CREATED,
    summary="Register a new user",
    description="Create a new user account with email, password, and company information."
)
async def register(
    user_data: UserCreate,
    db: AsyncSession = Depends(get_db)
) -> User:
    """
    Register a new user.
    
    - **email**: Valid email address (will be verified)
    - **password**: At least 8 characters with uppercase, lowercase, and digit
    - **company_name**: Company name (1-255 characters)
    - **company_size**: Optional company size (1-10, 10-50, 50-200, 200+)
    - **language**: Optional language preference (defaults to French)
    - **country**: Optional country (defaults to France)
    - **currency**: Optional currency (defaults to EUR)
    - **timezone**: Optional timezone (defaults to Europe/Paris)
    """
    try:
        user = await AuthService.register_user(db, user_data)
        return user
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.post(
    "/login",
    response_model=Token,
    summary="Login",
    description="Authenticate with email and password to get access token."
)
async def login(
    credentials: LoginRequest,
    db: AsyncSession = Depends(get_db)
) -> Token:
    """
    Login with email and password.
    
    Returns:
    - **access_token**: JWT access token (expires in 30 minutes)
    - **refresh_token**: JWT refresh token (expires in 7 days)
    - **token_type**: Token type (always "bearer")
    """
    user = await AuthService.authenticate_user(
        db,
        credentials.email,
        credentials.password
    )
    
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    tokens = AuthService.create_tokens(user)
    return tokens


@router.get(
    "/me",
    response_model=UserRead,
    summary="Get current user",
    description="Get the currently authenticated user's information."
)
async def get_me(
    current_user: User = Depends(get_current_user)
) -> User:
    """
    Get current authenticated user.
    
    Requires valid access token in Authorization header:
    `Authorization: Bearer <access_token>`
    """
    return current_user


@router.post(
    "/change-password",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Change password",
    description="Change the current user's password."
)
async def change_password(
    password_data: PasswordChange,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
) -> None:
    """
    Change current user's password.
    
    - **current_password**: Current password
    - **new_password**: New password (at least 8 characters with uppercase, lowercase, and digit)
    
    Requires valid access token.
    """
    try:
        await AuthService.change_password(
            db,
            current_user,
            password_data.current_password,
            password_data.new_password
        )
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )

