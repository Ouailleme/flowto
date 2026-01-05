"""Authentication service for user login, registration, and token management."""
from datetime import datetime, timedelta
from typing import Optional
from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
import logging

from app.models.user import User
from app.schemas.user import UserCreate
from app.core.security import (
    verify_password,
    hash_password,
    create_access_token,
    create_refresh_token,
    decode_token
)
from app.core.config import settings

logger = logging.getLogger(__name__)


class AuthService:
    """Service for authentication operations."""

    @staticmethod
    async def register(
        db: AsyncSession,
        user_data: UserCreate
    ) -> User:
        """
        Register a new user.
        
        Args:
            db: Database session
            user_data: User registration data
            
        Returns:
            Created user object
            
        Raises:
            ValueError: If email already exists
        """
        # Check if email already exists (case-insensitive)
        result = await db.execute(
            select(User).where(func.lower(User.email) == user_data.email.lower())
        )
        existing_user = result.scalar_one_or_none()
        
        if existing_user:
            raise ValueError("Email already exists")
        
        # Create new user with all fields
        user = User(
            email=user_data.email.lower(),
            hashed_password=hash_password(user_data.password),
            company_name=user_data.company_name,
            company_size=getattr(user_data, 'company_size', "1-10"),
            industry=getattr(user_data, 'industry', None),
            country=getattr(user_data, 'country', "FR"),
            language=getattr(user_data, 'language', "fr"),
            currency=getattr(user_data, 'currency', "EUR"),
            timezone=getattr(user_data, 'timezone', "Europe/Paris"),
            is_active=True,
            is_verified=False,
            subscription_plan="free",
            subscription_status="trial",
        )
        
        db.add(user)
        await db.commit()
        await db.refresh(user)
        
        logger.info(f"User registered: {user.email} (ID: {user.id})")
        return user

    @staticmethod
    async def login(
        db: AsyncSession,
        email: str,
        password: str
    ) -> dict:
        """
        Authenticate user and return tokens.
        
        Args:
            db: Database session
            email: User email
            password: Plain text password
            
        Returns:
            Dictionary with access_token, refresh_token, and token_type
            
        Raises:
            ValueError: If credentials are invalid or user is not verified/active
        """
        # Find user by email (case-insensitive)
        result = await db.execute(
            select(User).where(func.lower(User.email) == email.lower())
        )
        user = result.scalar_one_or_none()
        
        if not user:
            raise ValueError("Invalid credentials")
        
        # Verify password
        if not verify_password(password, user.hashed_password):
            raise ValueError("Invalid credentials")
        
        # Check if user is active
        if not user.is_active:
            raise ValueError("User account is inactive")
        
        # Check if user is verified
        if not user.is_verified:
            raise ValueError("Email is not verified")
        
        # Update last login timestamp
        user.last_login_at = datetime.utcnow()
        await db.commit()
        
        # Create tokens
        tokens = AuthService.create_tokens(user.id)
        
        logger.info(f"User logged in: {user.email} (ID: {user.id})")
        return tokens

    @staticmethod
    def create_tokens(user_id: UUID) -> dict:
        """
        Create access and refresh tokens for a user.
        
        Args:
            user_id: User UUID
            
        Returns:
            Dictionary with access_token, refresh_token, and token_type
        """
        access_token = create_access_token(
            data={"sub": str(user_id)},
            expires_delta=timedelta(minutes=settings.access_token_expire_minutes)
        )
        
        refresh_token = create_refresh_token(
            data={"sub": str(user_id)},
            expires_delta=timedelta(days=settings.refresh_token_expire_days)
        )
        
        return {
            "access_token": access_token,
            "refresh_token": refresh_token,
            "token_type": "bearer"
        }

    @staticmethod
    async def request_password_reset(
        db: AsyncSession,
        email: str
    ) -> Optional[str]:
        """
        Generate password reset token for a user.
        
        Args:
            db: Database session
            email: User email
            
        Returns:
            Password reset token if user exists, None otherwise
        """
        # Find user by email
        result = await db.execute(
            select(User).where(func.lower(User.email) == email.lower())
        )
        user = result.scalar_one_or_none()
        
        if not user:
            # Don't reveal if email exists (security)
            logger.warning(f"Password reset requested for non-existent email: {email}")
            return None
        
        # Create reset token (expires in 1 hour)
        reset_token = create_access_token(
            data={"sub": str(user.id), "type": "password_reset"},
            expires_delta=timedelta(hours=1)
        )
        
        logger.info(f"Password reset requested for: {user.email}")
        return reset_token

    @staticmethod
    async def reset_password(
        db: AsyncSession,
        token: str,
        new_password: str
    ) -> bool:
        """
        Reset user password with reset token.
        
        Args:
            db: Database session
            token: Password reset token
            new_password: New plain text password
            
        Returns:
            True if password was reset successfully, False otherwise
        """
        # Decode token
        payload = decode_token(token)
        
        if not payload or payload.get("type") != "password_reset":
            logger.warning("Invalid or expired password reset token")
            return False
        
        user_id = payload.get("sub")
        if not user_id:
            return False
        
        # Find user
        result = await db.execute(
            select(User).where(User.id == UUID(user_id))
        )
        user = result.scalar_one_or_none()
        
        if not user:
            return False
        
        # Update password
        user.hashed_password = hash_password(new_password)
        await db.commit()
        
        logger.info(f"Password reset successful for: {user.email}")
        return True

    @staticmethod
    async def send_verification_email(
        db: AsyncSession,
        user_id: UUID,
        sendgrid_client
    ) -> bool:
        """
        Send email verification link to user.
        
        Args:
            db: Database session
            user_id: User UUID
            sendgrid_client: SendGrid client instance
            
        Returns:
            True if email was sent successfully
        """
        user = await AuthService.get_user_by_id(db, user_id)
        
        if not user:
            return False
        
        # Create verification token (expires in 24 hours)
        verification_token = create_access_token(
            data={"sub": str(user.id), "type": "email_verification"},
            expires_delta=timedelta(hours=24)
        )
        
        # Send email (mock for now, will be implemented with SendGrid)
        try:
            await sendgrid_client.send_verification_email(
                to_email=user.email,
                token=verification_token
            )
            logger.info(f"Verification email sent to: {user.email}")
            return True
        except Exception as e:
            logger.error(f"Failed to send verification email: {e}")
            return False

    @staticmethod
    async def verify_email(
        db: AsyncSession,
        token: str
    ) -> bool:
        """
        Verify user email with verification token.
        
        Args:
            db: Database session
            token: Email verification token
            
        Returns:
            True if email was verified successfully, False otherwise
        """
        # Decode token
        payload = decode_token(token)
        
        if not payload or payload.get("type") != "email_verification":
            logger.warning("Invalid or expired email verification token")
            return False
        
        user_id = payload.get("sub")
        if not user_id:
            return False
        
        # Find user
        result = await db.execute(
            select(User).where(User.id == UUID(user_id))
        )
        user = result.scalar_one_or_none()
        
        if not user:
            return False
        
        # Mark email as verified
        user.is_verified = True
        user.email_verified_at = datetime.utcnow()
        await db.commit()
        
        logger.info(f"Email verified for: {user.email}")
        return True

    @staticmethod
    async def get_user_by_id(
        db: AsyncSession,
        user_id: UUID
    ) -> Optional[User]:
        """
        Get user by ID.
        
        Args:
            db: Database session
            user_id: User UUID
            
        Returns:
            User object if found, None otherwise
        """
        result = await db.execute(
            select(User).where(User.id == user_id)
        )
        return result.scalar_one_or_none()

    @staticmethod
    async def create_user(
        db: AsyncSession,
        user_data: UserCreate
    ) -> User:
        """Alias for register() - for API compatibility."""
        return await AuthService.register(db, user_data)
    
    @staticmethod
    async def authenticate_user(
        db: AsyncSession,
        email: str,
        password: str
    ) -> Optional[User]:
        """
        Authenticate a user with email and password (legacy method).
        Use login() instead for full authentication with tokens.
        
        Args:
            db: Database session
            email: User email
            password: Plain text password
            
        Returns:
            User object if authentication successful, None otherwise
        """
        result = await db.execute(
            select(User).where(func.lower(User.email) == email.lower())
        )
        user = result.scalar_one_or_none()
        
        if not user:
            return None
        
        if not verify_password(password, user.hashed_password):
            return None
        
        if not user.is_active:
            return None
        
        return user
