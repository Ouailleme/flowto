"""Integration tests for Auth API endpoints"""
import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.user import User


@pytest.mark.asyncio
async def test_register_success(client: AsyncClient, test_user_data):
    """Test successful user registration"""
    response = await client.post("/api/v1/auth/register", json=test_user_data)
    
    assert response.status_code == 201
    data = response.json()
    assert data["email"] == test_user_data["email"]
    assert data["company_name"] == test_user_data["company_name"]
    assert "id" in data
    assert "hashed_password" not in data  # Should not expose password


@pytest.mark.asyncio
async def test_register_duplicate_email(client: AsyncClient, test_user_data):
    """Test registration with duplicate email"""
    # First registration
    response1 = await client.post("/api/v1/auth/register", json=test_user_data)
    assert response1.status_code == 201
    
    # Second registration with same email
    response2 = await client.post("/api/v1/auth/register", json=test_user_data)
    assert response2.status_code == 400
    assert "already registered" in response2.json()["detail"].lower()


@pytest.mark.asyncio
async def test_register_invalid_email(client: AsyncClient, test_user_data):
    """Test registration with invalid email"""
    invalid_data = test_user_data.copy()
    invalid_data["email"] = "invalid-email"
    
    response = await client.post("/api/v1/auth/register", json=invalid_data)
    assert response.status_code == 422  # Validation error


@pytest.mark.asyncio
async def test_register_weak_password(client: AsyncClient, test_user_data):
    """Test registration with weak password"""
    weak_data = test_user_data.copy()
    weak_data["password"] = "weak"  # Too short, no uppercase, no digit
    
    response = await client.post("/api/v1/auth/register", json=weak_data)
    assert response.status_code == 422  # Validation error


@pytest.mark.asyncio
async def test_login_success(client: AsyncClient, test_user: User, test_user_data):
    """Test successful login"""
    login_data = {
        "email": test_user_data["email"],
        "password": test_user_data["password"]
    }
    
    response = await client.post("/api/v1/auth/login", json=login_data)
    
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert "refresh_token" in data
    assert data["token_type"] == "bearer"


@pytest.mark.asyncio
async def test_login_wrong_password(client: AsyncClient, test_user: User, test_user_data):
    """Test login with wrong password"""
    login_data = {
        "email": test_user_data["email"],
        "password": "WrongPassword123"
    }
    
    response = await client.post("/api/v1/auth/login", json=login_data)
    
    assert response.status_code == 401
    assert "incorrect" in response.json()["detail"].lower()


@pytest.mark.asyncio
async def test_login_nonexistent_user(client: AsyncClient):
    """Test login with non-existent email"""
    login_data = {
        "email": "nonexistent@example.com",
        "password": "Password123"
    }
    
    response = await client.post("/api/v1/auth/login", json=login_data)
    
    assert response.status_code == 401


@pytest.mark.asyncio
async def test_get_me_success(client: AsyncClient, test_user: User, auth_headers):
    """Test get current user endpoint"""
    response = await client.get("/api/v1/auth/me", headers=auth_headers)
    
    assert response.status_code == 200
    data = response.json()
    assert data["email"] == test_user.email
    assert data["id"] == str(test_user.id)


@pytest.mark.asyncio
async def test_get_me_no_token(client: AsyncClient):
    """Test get current user without token"""
    response = await client.get("/api/v1/auth/me")
    
    assert response.status_code == 403  # No credentials


@pytest.mark.asyncio
async def test_get_me_invalid_token(client: AsyncClient):
    """Test get current user with invalid token"""
    headers = {"Authorization": "Bearer invalid_token"}
    
    response = await client.get("/api/v1/auth/me", headers=headers)
    
    assert response.status_code == 401


@pytest.mark.asyncio
async def test_change_password_success(client: AsyncClient, test_user_data, auth_headers):
    """Test successful password change"""
    password_data = {
        "current_password": test_user_data["password"],
        "new_password": "NewSecurePass789"
    }
    
    response = await client.post(
        "/api/v1/auth/change-password",
        json=password_data,
        headers=auth_headers
    )
    
    assert response.status_code == 204


@pytest.mark.asyncio
async def test_change_password_wrong_current(client: AsyncClient, auth_headers):
    """Test password change with wrong current password"""
    password_data = {
        "current_password": "WrongPassword123",
        "new_password": "NewSecurePass789"
    }
    
    response = await client.post(
        "/api/v1/auth/change-password",
        json=password_data,
        headers=auth_headers
    )
    
    assert response.status_code == 400
    assert "incorrect" in response.json()["detail"].lower()


@pytest.mark.asyncio
async def test_complete_auth_flow(client: AsyncClient, test_user_data):
    """Test complete authentication flow: register → login → get me"""
    # 1. Register
    register_response = await client.post("/api/v1/auth/register", json=test_user_data)
    assert register_response.status_code == 201
    
    # 2. Login
    login_data = {
        "email": test_user_data["email"],
        "password": test_user_data["password"]
    }
    login_response = await client.post("/api/v1/auth/login", json=login_data)
    assert login_response.status_code == 200
    
    tokens = login_response.json()
    headers = {"Authorization": f"Bearer {tokens['access_token']}"}
    
    # 3. Get me
    me_response = await client.get("/api/v1/auth/me", headers=headers)
    assert me_response.status_code == 200
    
    user_data = me_response.json()
    assert user_data["email"] == test_user_data["email"]

