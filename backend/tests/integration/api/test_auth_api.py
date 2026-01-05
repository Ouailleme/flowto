"""
Integration tests for Auth API endpoints.
Tests the complete flow from HTTP request to database.
"""
import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
@pytest.mark.integration
async def test_register_endpoint_success(client: AsyncClient):
    """Test successful user registration via API."""
    response = await client.post(
        "/api/v1/auth/register",
        json={
            "email": "newuser@test.com",
            "password": "TestPassword123!",
            "company_name": "Test Company"
        }
    )
    
    assert response.status_code == 201
    data = response.json()
    assert "user" in data
    assert "access_token" in data
    assert "refresh_token" in data
    assert data["user"]["email"] == "newuser@test.com"
    assert data["user"]["id"] is not None
    assert "hashed_password" not in data["user"]  # Should not expose password


@pytest.mark.asyncio
@pytest.mark.integration
async def test_register_endpoint_duplicate_email(client: AsyncClient, test_user):
    """Test registration fails with duplicate email."""
    response = await client.post(
        "/api/v1/auth/register",
        json={
            "email": test_user.email,
            "password": "TestPassword123!",
            "company_name": "Another Company"
        }
    )
    
    assert response.status_code == 400
    assert "already exists" in response.json()["detail"].lower()


@pytest.mark.asyncio
@pytest.mark.integration
async def test_register_endpoint_invalid_email(client: AsyncClient):
    """Test registration fails with invalid email."""
    response = await client.post(
        "/api/v1/auth/register",
        json={
            "email": "invalid-email",
            "password": "TestPassword123!",
            "company_name": "Test Company"
        }
    )
    
    assert response.status_code == 422  # Validation error


@pytest.mark.asyncio
@pytest.mark.integration
async def test_register_endpoint_missing_fields(client: AsyncClient):
    """Test registration fails with missing required fields."""
    response = await client.post(
        "/api/v1/auth/register",
        json={
            "email": "test@test.com"
            # Missing password and company_name
        }
    )
    
    assert response.status_code == 422


@pytest.mark.asyncio
@pytest.mark.integration
async def test_login_endpoint_success(client: AsyncClient, test_user):
    """Test successful login via API."""
    response = await client.post(
        "/api/v1/auth/login",
        json={
            "email": test_user.email,
            "password": "TestPassword123!"
        }
    )
    
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert "refresh_token" in data
    assert data["token_type"] == "bearer"


@pytest.mark.asyncio
@pytest.mark.integration
async def test_login_endpoint_wrong_password(client: AsyncClient, test_user):
    """Test login fails with wrong password."""
    response = await client.post(
        "/api/v1/auth/login",
        json={
            "email": test_user.email,
            "password": "WrongPassword123!"
        }
    )
    
    assert response.status_code == 401
    # Error message varies, just check it's unauthorized
    assert "detail" in response.json()


@pytest.mark.asyncio
@pytest.mark.integration
async def test_login_endpoint_nonexistent_user(client: AsyncClient):
    """Test login fails with non-existent user."""
    response = await client.post(
        "/api/v1/auth/login",
        json={
            "email": "nonexistent@test.com",
            "password": "TestPassword123!"
        }
    )
    
    assert response.status_code == 401


@pytest.mark.asyncio
@pytest.mark.integration
async def test_login_endpoint_unverified_user(client: AsyncClient, test_user_unverified):
    """Test login succeeds but user is marked as unverified."""
    # Note: Current implementation allows login for unverified users
    # They just have is_verified=False in their user object
    response = await client.post(
        "/api/v1/auth/login",
        json={
            "email": test_user_unverified.email,
            "password": "TestPassword123!"
        }
    )
    
    assert response.status_code == 200
    data = response.json()
    assert data["user"]["is_verified"] is False
    assert "access_token" in data


@pytest.mark.asyncio
@pytest.mark.integration
async def test_complete_auth_flow(client: AsyncClient):
    """Test complete authentication flow: register → login."""
    # 1. Register
    register_response = await client.post(
        "/api/v1/auth/register",
        json={
            "email": "flow@test.com",
            "password": "TestPassword123!",
            "company_name": "Flow Company"
        }
    )
    assert register_response.status_code == 201
    register_data = register_response.json()
    assert "user" in register_data
    assert register_data["user"]["email"] == "flow@test.com"
    user_id = register_data["user"]["id"]
    
    # 2. Login (user can login even if not verified in current implementation)
    login_response = await client.post(
        "/api/v1/auth/login",
        json={
            "email": "flow@test.com",
            "password": "TestPassword123!"
        }
    )
    assert login_response.status_code == 200
    login_data = login_response.json()
    assert "access_token" in login_data
    assert "refresh_token" in login_data
    assert login_data["user"]["email"] == "flow@test.com"
    assert login_data["user"]["id"] == user_id

