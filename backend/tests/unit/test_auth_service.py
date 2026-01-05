"""Unit tests for AuthService"""
import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from app.services.auth_service import AuthService
from app.schemas.user import UserCreate
from app.models.user import User, LanguageEnum, CurrencyEnum, CountryEnum


@pytest.mark.asyncio
async def test_register_user_success(db_session: AsyncSession, test_user_data):
    """Test successful user registration"""
    user_create = UserCreate(**test_user_data)
    
    user = await AuthService.register_user(db_session, user_create)
    
    assert user.id is not None
    assert user.email == test_user_data["email"]
    assert user.company_name == test_user_data["company_name"]
    assert user.language == LanguageEnum.FRENCH
    assert user.currency == CurrencyEnum.EUR
    assert user.country == CountryEnum.FRANCE
    assert user.is_active is True
    assert user.is_verified is False
    assert user.subscription_plan == "trial"
    assert user.hashed_password != test_user_data["password"]  # Should be hashed


@pytest.mark.asyncio
async def test_register_user_duplicate_email(db_session: AsyncSession, test_user_data):
    """Test registration with duplicate email fails"""
    user_create = UserCreate(**test_user_data)
    
    # Register first user
    await AuthService.register_user(db_session, user_create)
    await db_session.commit()
    
    # Try to register with same email
    with pytest.raises(ValueError, match="Email already registered"):
        await AuthService.register_user(db_session, user_create)


@pytest.mark.asyncio
async def test_register_user_international_defaults(db_session: AsyncSession):
    """Test registration with international settings"""
    user_data = {
        "email": "user@example.com",
        "password": "SecurePass123",
        "company_name": "International Co",
        "language": "en",
        "country": "US",
        "currency": "USD",
        "timezone": "America/New_York"
    }
    user_create = UserCreate(**user_data)
    
    user = await AuthService.register_user(db_session, user_create)
    
    assert user.language == LanguageEnum.ENGLISH
    assert user.currency == CurrencyEnum.USD
    assert user.country == CountryEnum.USA
    assert user.timezone == "America/New_York"
    assert user.locale == "en_US"


@pytest.mark.asyncio
async def test_authenticate_user_success(db_session: AsyncSession, test_user: User, test_user_data):
    """Test successful authentication"""
    user = await AuthService.authenticate_user(
        db_session,
        test_user_data["email"],
        test_user_data["password"]
    )
    
    assert user is not None
    assert user.id == test_user.id
    assert user.email == test_user.email


@pytest.mark.asyncio
async def test_authenticate_user_wrong_password(db_session: AsyncSession, test_user: User, test_user_data):
    """Test authentication with wrong password"""
    user = await AuthService.authenticate_user(
        db_session,
        test_user_data["email"],
        "WrongPassword123"
    )
    
    assert user is None


@pytest.mark.asyncio
async def test_authenticate_user_nonexistent_email(db_session: AsyncSession):
    """Test authentication with non-existent email"""
    user = await AuthService.authenticate_user(
        db_session,
        "nonexistent@example.com",
        "Password123"
    )
    
    assert user is None


@pytest.mark.asyncio
async def test_create_tokens(test_user: User):
    """Test token creation"""
    tokens = AuthService.create_tokens(test_user)
    
    assert tokens.access_token is not None
    assert tokens.refresh_token is not None
    assert tokens.token_type == "bearer"


@pytest.mark.asyncio
async def test_get_user_by_id(db_session: AsyncSession, test_user: User):
    """Test get user by ID"""
    user = await AuthService.get_user_by_id(db_session, test_user.id)
    
    assert user is not None
    assert user.id == test_user.id


@pytest.mark.asyncio
async def test_get_user_by_email(db_session: AsyncSession, test_user: User):
    """Test get user by email"""
    user = await AuthService.get_user_by_email(db_session, test_user.email)
    
    assert user is not None
    assert user.email == test_user.email


@pytest.mark.asyncio
async def test_change_password_success(db_session: AsyncSession, test_user: User, test_user_data):
    """Test successful password change"""
    new_password = "NewSecurePass456"
    
    result = await AuthService.change_password(
        db_session,
        test_user,
        test_user_data["password"],
        new_password
    )
    
    assert result is True
    
    # Verify old password doesn't work
    user = await AuthService.authenticate_user(
        db_session,
        test_user.email,
        test_user_data["password"]
    )
    assert user is None
    
    # Verify new password works
    await db_session.commit()
    user = await AuthService.authenticate_user(
        db_session,
        test_user.email,
        new_password
    )
    assert user is not None


@pytest.mark.asyncio
async def test_change_password_wrong_current(db_session: AsyncSession, test_user: User):
    """Test password change with wrong current password"""
    with pytest.raises(ValueError, match="Current password is incorrect"):
        await AuthService.change_password(
            db_session,
            test_user,
            "WrongPassword",
            "NewPassword123"
        )

