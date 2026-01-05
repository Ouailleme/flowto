"""
Unit tests for AuthService.
Tests all authentication operations including registration, login, password reset, etc.
Target: 100% code coverage
"""
import pytest
from datetime import datetime, timedelta
from uuid import UUID, uuid4
from unittest.mock import Mock, AsyncMock, patch

from app.services.auth_service import AuthService
from app.schemas.user import UserCreate
from app.models.user import User
from app.core.security import verify_password, decode_token


# ============================================================================
# REGISTRATION TESTS
# ============================================================================

@pytest.mark.asyncio
@pytest.mark.unit
async def test_register_success(db_session):
    """Test successful user registration."""
    user_data = UserCreate(
        email="newuser@example.com",
        password="SecurePassword123!",
        company_name="Test Company"
    )
    
    user = await AuthService.register(db_session, user_data)
    
    assert user.id is not None
    assert user.email == "newuser@example.com"
    assert user.company_name == "Test Company"
    assert user.is_active is True
    assert user.is_verified is False
    assert user.subscription_plan == "free"
    assert verify_password("SecurePassword123!", user.hashed_password)


@pytest.mark.asyncio
@pytest.mark.unit
async def test_register_email_case_insensitive(db_session):
    """Test that registration treats email as case-insensitive."""
    user_data = UserCreate(
        email="TestUser@EXAMPLE.COM",
        password="SecurePassword123!",
        company_name="Test Company"
    )
    
    user = await AuthService.register(db_session, user_data)
    
    # Email should be stored in lowercase
    assert user.email == "testuser@example.com"


@pytest.mark.asyncio
@pytest.mark.unit
async def test_register_duplicate_email(db_session, test_user):
    """Test registration fails with duplicate email."""
    user_data = UserCreate(
        email=test_user.email,
        password="AnotherPassword123!",
        company_name="Another Company"
    )
    
    with pytest.raises(ValueError, match="Email already exists"):
        await AuthService.register(db_session, user_data)


@pytest.mark.asyncio
@pytest.mark.unit
async def test_register_duplicate_email_case_insensitive(db_session, test_user):
    """Test registration fails with duplicate email (case-insensitive)."""
    user_data = UserCreate(
        email=test_user.email.upper(),  # Same email but uppercase
        password="AnotherPassword123!",
        company_name="Another Company"
    )
    
    with pytest.raises(ValueError, match="Email already exists"):
        await AuthService.register(db_session, user_data)


@pytest.mark.asyncio
@pytest.mark.unit
async def test_register_with_optional_fields(db_session):
    """Test registration with optional fields."""
    user_data = UserCreate(
        email="user@example.com",
        password="Password123!",
        company_name="My Company",
        company_size="50-100",
        country="US",
        language="en",
        currency="USD"
    )
    
    user = await AuthService.register(db_session, user_data)
    
    assert user.company_size == "50-100"
    assert user.country == "US"
    assert user.language == "en"
    assert user.currency == "USD"


# ============================================================================
# LOGIN TESTS
# ============================================================================

@pytest.mark.asyncio
@pytest.mark.unit
async def test_login_success(db_session, test_user):
    """Test successful login."""
    tokens = await AuthService.login(
        db_session,
        email=test_user.email,
        password="TestPassword123!"
    )
    
    assert "access_token" in tokens
    assert "refresh_token" in tokens
    assert tokens["token_type"] == "bearer"
    
    # Verify tokens are valid
    access_payload = decode_token(tokens["access_token"])
    assert access_payload is not None
    assert access_payload["sub"] == str(test_user.id)


@pytest.mark.asyncio
@pytest.mark.unit
async def test_login_email_case_insensitive(db_session, test_user):
    """Test login works with different email case."""
    tokens = await AuthService.login(
        db_session,
        email=test_user.email.upper(),  # Uppercase email
        password="TestPassword123!"
    )
    
    assert "access_token" in tokens
    assert tokens["token_type"] == "bearer"


@pytest.mark.asyncio
@pytest.mark.unit
async def test_login_invalid_email(db_session):
    """Test login fails with invalid email."""
    with pytest.raises(ValueError, match="Invalid credentials"):
        await AuthService.login(
            db_session,
            email="nonexistent@example.com",
            password="AnyPassword123!"
        )


@pytest.mark.asyncio
@pytest.mark.unit
async def test_login_wrong_password(db_session, test_user):
    """Test login fails with wrong password."""
    with pytest.raises(ValueError, match="Invalid credentials"):
        await AuthService.login(
            db_session,
            email=test_user.email,
            password="WrongPassword123!"
        )


@pytest.mark.asyncio
@pytest.mark.unit
async def test_login_inactive_user(db_session, test_user):
    """Test login fails for inactive user."""
    # Make user inactive
    test_user.is_active = False
    await db_session.commit()
    
    with pytest.raises(ValueError, match="User account is inactive"):
        await AuthService.login(
            db_session,
            email=test_user.email,
            password="TestPassword123!"
        )


@pytest.mark.asyncio
@pytest.mark.unit
async def test_login_unverified_user(db_session, test_user_unverified):
    """Test login fails for unverified user."""
    with pytest.raises(ValueError, match="Email is not verified"):
        await AuthService.login(
            db_session,
            email=test_user_unverified.email,
            password="TestPassword123!"
        )


@pytest.mark.asyncio
@pytest.mark.unit
async def test_login_updates_last_login(db_session, test_user):
    """Test that login updates last_login_at timestamp."""
    original_last_login = test_user.last_login_at
    
    await AuthService.login(
        db_session,
        email=test_user.email,
        password="TestPassword123!"
    )
    
    await db_session.refresh(test_user)
    assert test_user.last_login_at is not None
    assert test_user.last_login_at != original_last_login


# ============================================================================
# CREATE TOKENS TESTS
# ============================================================================

@pytest.mark.unit
def test_create_tokens():
    """Test token creation."""
    user_id = uuid4()
    
    tokens = AuthService.create_tokens(user_id)
    
    assert "access_token" in tokens
    assert "refresh_token" in tokens
    assert tokens["token_type"] == "bearer"
    
    # Verify tokens contain correct user_id
    access_payload = decode_token(tokens["access_token"])
    refresh_payload = decode_token(tokens["refresh_token"])
    
    assert access_payload["sub"] == str(user_id)
    assert refresh_payload["sub"] == str(user_id)


# ============================================================================
# PASSWORD RESET TESTS
# ============================================================================

@pytest.mark.asyncio
@pytest.mark.unit
async def test_request_password_reset_success(db_session, test_user):
    """Test successful password reset request."""
    reset_token = await AuthService.request_password_reset(
        db_session,
        email=test_user.email
    )
    
    assert reset_token is not None
    
    # Verify token contains correct data
    payload = decode_token(reset_token)
    assert payload is not None
    assert payload["sub"] == str(test_user.id)
    assert payload["type"] == "password_reset"


@pytest.mark.asyncio
@pytest.mark.unit
async def test_request_password_reset_nonexistent_email(db_session):
    """Test password reset request for non-existent email returns None."""
    reset_token = await AuthService.request_password_reset(
        db_session,
        email="nonexistent@example.com"
    )
    
    # Should return None (security: don't reveal if email exists)
    assert reset_token is None


@pytest.mark.asyncio
@pytest.mark.unit
async def test_request_password_reset_case_insensitive(db_session, test_user):
    """Test password reset request with different email case."""
    reset_token = await AuthService.request_password_reset(
        db_session,
        email=test_user.email.upper()
    )
    
    assert reset_token is not None
    payload = decode_token(reset_token)
    assert payload["sub"] == str(test_user.id)


@pytest.mark.asyncio
@pytest.mark.unit
async def test_reset_password_success(db_session, test_user):
    """Test successful password reset."""
    # Generate reset token
    reset_token = await AuthService.request_password_reset(
        db_session,
        email=test_user.email
    )
    
    # Reset password
    new_password = "NewSecurePassword123!"
    success = await AuthService.reset_password(
        db_session,
        token=reset_token,
        new_password=new_password
    )
    
    assert success is True
    
    # Verify new password works
    await db_session.refresh(test_user)
    assert verify_password(new_password, test_user.hashed_password)


@pytest.mark.asyncio
@pytest.mark.unit
async def test_reset_password_invalid_token(db_session):
    """Test password reset fails with invalid token."""
    success = await AuthService.reset_password(
        db_session,
        token="invalid_token_xyz",
        new_password="NewPassword123!"
    )
    
    assert success is False


@pytest.mark.asyncio
@pytest.mark.unit
async def test_reset_password_wrong_token_type(db_session, test_user):
    """Test password reset fails with wrong token type."""
    # Create access token instead of password_reset token
    from app.core.security import create_access_token
    wrong_token = create_access_token(
        data={"sub": str(test_user.id), "type": "email_verification"},
        expires_delta=timedelta(hours=1)
    )
    
    success = await AuthService.reset_password(
        db_session,
        token=wrong_token,
        new_password="NewPassword123!"
    )
    
    assert success is False


@pytest.mark.asyncio
@pytest.mark.unit
async def test_reset_password_expired_token(db_session, test_user):
    """Test password reset fails with expired token."""
    # Create expired token (expired 1 hour ago)
    from app.core.security import create_access_token
    expired_token = create_access_token(
        data={"sub": str(test_user.id), "type": "password_reset"},
        expires_delta=timedelta(hours=-1)  # Negative = expired
    )
    
    success = await AuthService.reset_password(
        db_session,
        token=expired_token,
        new_password="NewPassword123!"
    )
    
    assert success is False


@pytest.mark.asyncio
@pytest.mark.unit
async def test_reset_password_nonexistent_user(db_session):
    """Test password reset fails for non-existent user."""
    from app.core.security import create_access_token
    fake_user_id = uuid4()
    token = create_access_token(
        data={"sub": str(fake_user_id), "type": "password_reset"},
        expires_delta=timedelta(hours=1)
    )
    
    success = await AuthService.reset_password(
        db_session,
        token=token,
        new_password="NewPassword123!"
    )
    
    assert success is False


# ============================================================================
# EMAIL VERIFICATION TESTS
# ============================================================================

@pytest.mark.asyncio
@pytest.mark.unit
async def test_send_verification_email_success(db_session, test_user):
    """Test successful verification email sending."""
    # Mock sendgrid client
    mock_sendgrid = AsyncMock()
    mock_sendgrid.send_verification_email = AsyncMock(return_value=True)
    
    success = await AuthService.send_verification_email(
        db_session,
        user_id=test_user.id,
        sendgrid_client=mock_sendgrid
    )
    
    assert success is True
    mock_sendgrid.send_verification_email.assert_called_once()


@pytest.mark.asyncio
@pytest.mark.unit
async def test_send_verification_email_nonexistent_user(db_session):
    """Test verification email fails for non-existent user."""
    mock_sendgrid = AsyncMock()
    
    success = await AuthService.send_verification_email(
        db_session,
        user_id=uuid4(),  # Random UUID that doesn't exist
        sendgrid_client=mock_sendgrid
    )
    
    assert success is False


@pytest.mark.asyncio
@pytest.mark.unit
async def test_send_verification_email_sendgrid_failure(db_session, test_user):
    """Test verification email handles sendgrid failure."""
    # Mock sendgrid client that raises exception
    mock_sendgrid = AsyncMock()
    mock_sendgrid.send_verification_email = AsyncMock(
        side_effect=Exception("SendGrid API error")
    )
    
    success = await AuthService.send_verification_email(
        db_session,
        user_id=test_user.id,
        sendgrid_client=mock_sendgrid
    )
    
    assert success is False


@pytest.mark.asyncio
@pytest.mark.unit
async def test_verify_email_success(db_session, test_user_unverified):
    """Test successful email verification."""
    # Create verification token
    from app.core.security import create_access_token
    verification_token = create_access_token(
        data={"sub": str(test_user_unverified.id), "type": "email_verification"},
        expires_delta=timedelta(hours=24)
    )
    
    success = await AuthService.verify_email(
        db_session,
        token=verification_token
    )
    
    assert success is True
    
    # Verify user is now verified
    await db_session.refresh(test_user_unverified)
    assert test_user_unverified.is_verified is True
    assert test_user_unverified.email_verified_at is not None


@pytest.mark.asyncio
@pytest.mark.unit
async def test_verify_email_invalid_token(db_session):
    """Test email verification fails with invalid token."""
    success = await AuthService.verify_email(
        db_session,
        token="invalid_token_xyz"
    )
    
    assert success is False


@pytest.mark.asyncio
@pytest.mark.unit
async def test_verify_email_wrong_token_type(db_session, test_user_unverified):
    """Test email verification fails with wrong token type."""
    from app.core.security import create_access_token
    wrong_token = create_access_token(
        data={"sub": str(test_user_unverified.id), "type": "password_reset"},
        expires_delta=timedelta(hours=1)
    )
    
    success = await AuthService.verify_email(
        db_session,
        token=wrong_token
    )
    
    assert success is False


@pytest.mark.asyncio
@pytest.mark.unit
async def test_verify_email_expired_token(db_session, test_user_unverified):
    """Test email verification fails with expired token."""
    from app.core.security import create_access_token
    expired_token = create_access_token(
        data={"sub": str(test_user_unverified.id), "type": "email_verification"},
        expires_delta=timedelta(hours=-1)
    )
    
    success = await AuthService.verify_email(
        db_session,
        token=expired_token
    )
    
    assert success is False


@pytest.mark.asyncio
@pytest.mark.unit
async def test_verify_email_nonexistent_user(db_session):
    """Test email verification fails for non-existent user."""
    from app.core.security import create_access_token
    fake_user_id = uuid4()
    token = create_access_token(
        data={"sub": str(fake_user_id), "type": "email_verification"},
        expires_delta=timedelta(hours=24)
    )
    
    success = await AuthService.verify_email(
        db_session,
        token=token
    )
    
    assert success is False


# ============================================================================
# GET USER TESTS
# ============================================================================

@pytest.mark.asyncio
@pytest.mark.unit
async def test_get_user_by_id_success(db_session, test_user):
    """Test successful user retrieval by ID."""
    user = await AuthService.get_user_by_id(db_session, test_user.id)
    
    assert user is not None
    assert user.id == test_user.id
    assert user.email == test_user.email


@pytest.mark.asyncio
@pytest.mark.unit
async def test_get_user_by_id_not_found(db_session):
    """Test get_user_by_id returns None for non-existent user."""
    user = await AuthService.get_user_by_id(db_session, uuid4())
    
    assert user is None


# ============================================================================
# AUTHENTICATE USER (LEGACY) TESTS
# ============================================================================

@pytest.mark.asyncio
@pytest.mark.unit
async def test_authenticate_user_success(db_session, test_user):
    """Test successful user authentication (legacy method)."""
    user = await AuthService.authenticate_user(
        db_session,
        email=test_user.email,
        password="TestPassword123!"
    )
    
    assert user is not None
    assert user.id == test_user.id


@pytest.mark.asyncio
@pytest.mark.unit
async def test_authenticate_user_invalid_email(db_session):
    """Test authenticate_user returns None for invalid email."""
    user = await AuthService.authenticate_user(
        db_session,
        email="nonexistent@example.com",
        password="AnyPassword123!"
    )
    
    assert user is None


@pytest.mark.asyncio
@pytest.mark.unit
async def test_authenticate_user_wrong_password(db_session, test_user):
    """Test authenticate_user returns None for wrong password."""
    user = await AuthService.authenticate_user(
        db_session,
        email=test_user.email,
        password="WrongPassword123!"
    )
    
    assert user is None


@pytest.mark.asyncio
@pytest.mark.unit
async def test_authenticate_user_inactive(db_session, test_user):
    """Test authenticate_user returns None for inactive user."""
    test_user.is_active = False
    await db_session.commit()
    
    user = await AuthService.authenticate_user(
        db_session,
        email=test_user.email,
        password="TestPassword123!"
    )
    
    assert user is None


@pytest.mark.asyncio
@pytest.mark.unit
async def test_authenticate_user_case_insensitive(db_session, test_user):
    """Test authenticate_user works with different email case."""
    user = await AuthService.authenticate_user(
        db_session,
        email=test_user.email.upper(),
        password="TestPassword123!"
    )
    
    assert user is not None
    assert user.id == test_user.id
