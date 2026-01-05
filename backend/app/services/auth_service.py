"""Authentication service - Business logic"""
from typing import Optional, Tuple
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from uuid import UUID
import logging

from app.models.user import User, LanguageEnum, CurrencyEnum, CountryEnum
from app.schemas.user import UserCreate
from app.schemas.auth import Token
from app.core.security import (
    verify_password,
    get_password_hash,
    create_access_token,
    create_refresh_token,
)

logger = logging.getLogger(__name__)


class AuthService:
    """Authentication service"""
    
    @staticmethod
    async def register_user(
        db: AsyncSession,
        user_data: UserCreate
    ) -> User:
        """
        Register a new user.
        
        Args:
            db: Database session
            user_data: User registration data
            
        Returns:
            Created user
            
        Raises:
            ValueError: If email already exists
        """
        # Check if email already exists
        result = await db.execute(
            select(User).where(User.email == user_data.email)
        )
        existing_user = result.scalar_one_or_none()
        
        if existing_user is not None:
            raise ValueError("Email already registered")
        
        # Set defaults for international settings
        language = user_data.language or LanguageEnum.FRENCH
        country = user_data.country or CountryEnum.FRANCE
        currency = user_data.currency or CurrencyEnum.EUR
        timezone = user_data.timezone or "Europe/Paris"
        
        # Derive locale from language
        locale_map = {
            LanguageEnum.FRENCH: "fr_FR",
            LanguageEnum.ENGLISH: "en_US",
            LanguageEnum.SPANISH: "es_ES",
            LanguageEnum.GERMAN: "de_DE",
            LanguageEnum.ITALIAN: "it_IT",
            LanguageEnum.DUTCH: "nl_NL",
        }
        locale = locale_map.get(language, "fr_FR")
        
        # Create user
        user = User(
            email=user_data.email,
            hashed_password=get_password_hash(user_data.password),
            company_name=user_data.company_name,
            company_size=user_data.company_size,
            language=language,
            country=country,
            currency=currency,
            timezone=timezone,
            locale=locale,
            subscription_plan="trial",
            subscription_status="active",
            is_active=True,
            is_verified=False,  # Will be verified via email
            is_onboarded=False,
        )
        
        db.add(user)
        await db.flush()  # Get ID without committing
        
        logger.info(f"User registered: {user.email} (ID: {user.id})")
        
        return user
    
    @staticmethod
    async def authenticate_user(
        db: AsyncSession,
        email: str,
        password: str
    ) -> Optional[User]:
        """
        Authenticate a user with email and password.
        
        Args:
            db: Database session
            email: User email
            password: Plain text password
            
        Returns:
            User if authentication successful, None otherwise
        """
        # Get user by email
        result = await db.execute(
            select(User).where(
                User.email == email,
                User.deleted_at.is_(None)
            )
        )
        user = result.scalar_one_or_none()
        
        if user is None:
            logger.warning(f"Login attempt for non-existent email: {email}")
            return None
        
        # Verify password
        if not verify_password(password, user.hashed_password):
            logger.warning(f"Invalid password attempt for user: {email}")
            return None
        
        if not user.is_active:
            logger.warning(f"Login attempt for inactive user: {email}")
            return None
        
        logger.info(f"User authenticated: {email}")
        return user
    
    @staticmethod
    def create_tokens(user: User) -> Token:
        """
        Create access and refresh tokens for user.
        
        Args:
            user: User object
            
        Returns:
            Token object with access_token and refresh_token
        """
        access_token = create_access_token(
            data={"sub": str(user.id), "email": user.email}
        )
        refresh_token = create_refresh_token(
            data={"sub": str(user.id)}
        )
        
        return Token(
            access_token=access_token,
            refresh_token=refresh_token,
            token_type="bearer"
        )
    
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
            User if found, None otherwise
        """
        result = await db.execute(
            select(User).where(
                User.id == user_id,
                User.deleted_at.is_(None)
            )
        )
        return result.scalar_one_or_none()
    
    @staticmethod
    async def get_user_by_email(
        db: AsyncSession,
        email: str
    ) -> Optional[User]:
        """
        Get user by email.
        
        Args:
            db: Database session
            email: User email
            
        Returns:
            User if found, None otherwise
        """
        result = await db.execute(
            select(User).where(
                User.email == email,
                User.deleted_at.is_(None)
            )
        )
        return result.scalar_one_or_none()
    
    @staticmethod
    async def change_password(
        db: AsyncSession,
        user: User,
        current_password: str,
        new_password: str
    ) -> bool:
        """
        Change user password.
        
        Args:
            db: Database session
            user: User object
            current_password: Current plain text password
            new_password: New plain text password
            
        Returns:
            True if password changed successfully
            
        Raises:
            ValueError: If current password is incorrect
        """
        # Verify current password
        if not verify_password(current_password, user.hashed_password):
            raise ValueError("Current password is incorrect")
        
        # Update password
        user.hashed_password = get_password_hash(new_password)
        await db.flush()
        
        logger.info(f"Password changed for user: {user.email}")
        return True

