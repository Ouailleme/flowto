"""Authentication API endpoints"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.schemas.user import UserCreate
from app.schemas.auth import LoginRequest, LoginResponse, TokenResponse, UserResponse
from app.services.auth_service import AuthService
from app.models.user import User

router = APIRouter(prefix="/auth", tags=["authentication"])


@router.post(
    "/register",
    response_model=LoginResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Register a new user",
    description="Create a new user account with email and password."
)
async def register(
    user_data: UserCreate,
    db: AsyncSession = Depends(get_db)
) -> LoginResponse:
    """
    Register a new user and return tokens.
    
    - **email**: Valid email address
    - **password**: At least 6 characters
    - **full_name**: Optional full name
    """
    try:
        user = await AuthService.create_user(db, user_data)
        tokens = AuthService.create_tokens(user.id)
        
        return LoginResponse(
            user=UserResponse(
                id=str(user.id),
                email=user.email,
                full_name=user.full_name,
                is_active=user.is_active,
                is_verified=user.is_verified
            ),
            access_token=tokens["access_token"],
            refresh_token=tokens["refresh_token"],
            token_type=tokens["token_type"]
        )
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.post(
    "/login",
    response_model=LoginResponse,
    summary="Login",
    description="Authenticate with email and password to get access token."
)
async def login(
    credentials: LoginRequest,
    db: AsyncSession = Depends(get_db)
) -> LoginResponse:
    """
    Login with email and password.
    
    Returns:
    - **user**: User information
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
    
    tokens = AuthService.create_tokens(user.id)
    
    return LoginResponse(
        user=UserResponse(
            id=str(user.id),
            email=user.email,
            full_name=user.full_name,
            is_active=user.is_active,
            is_verified=user.is_verified
        ),
        access_token=tokens["access_token"],
        refresh_token=tokens["refresh_token"],
        token_type=tokens["token_type"]
    )


@router.get(
    "/me",
    response_model=UserResponse,
    summary="Get current user",
    description="Get the currently authenticated user's information."
)
async def get_me(
    db: AsyncSession = Depends(get_db)
) -> UserResponse:
    """
    Get current authenticated user.
    
    Requires valid access token in Authorization header:
    `Authorization: Bearer <access_token>`
    
    TODO: Implement JWT token verification
    """
    # For now, return demo user
    user = await AuthService.get_user_by_id(
        db,
        "a0eebc99-9c0b-4ef8-bb6d-6bb9bd380a11"  # Demo user ID
    )
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated"
        )
    
    return UserResponse(
        id=str(user.id),
        email=user.email,
        full_name=user.full_name,
        is_active=user.is_active,
        is_verified=user.is_verified
    )

