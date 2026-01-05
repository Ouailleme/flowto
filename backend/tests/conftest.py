"""Pytest configuration and fixtures"""
import pytest
import pytest_asyncio
from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from httpx import AsyncClient
import os

from app.main import app
from app.core.database import Base, get_db
from app.models.user import User

# Test database URL (SQLite for tests)
TEST_DATABASE_URL = "sqlite+aiosqlite:///:memory:"

# Create test engine
test_engine = create_async_engine(
    TEST_DATABASE_URL,
    echo=False,
    future=True,
)

# Create test session factory
TestSessionLocal = async_sessionmaker(
    test_engine,
    class_=AsyncSession,
    expire_on_commit=False,
)


@pytest_asyncio.fixture(scope="function")
async def db_session() -> AsyncGenerator[AsyncSession, None]:
    """
    Create a fresh database for each test function.
    
    Usage:
        async def test_something(db_session):
            user = User(email="test@test.com")
            db_session.add(user)
            await db_session.commit()
    """
    # Create tables
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    
    # Create session
    async with TestSessionLocal() as session:
        yield session
        await session.rollback()
    
    # Drop tables
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


@pytest_asyncio.fixture(scope="function")
async def client(db_session: AsyncSession) -> AsyncGenerator[AsyncClient, None]:
    """
    Create a test client with overridden database dependency.
    
    Usage:
        async def test_endpoint(client):
            response = await client.get("/api/v1/auth/me")
            assert response.status_code == 200
    """
    async def override_get_db():
        yield db_session
    
    app.dependency_overrides[get_db] = override_get_db
    
    async with AsyncClient(app=app, base_url="http://test") as ac:
        yield ac
    
    app.dependency_overrides.clear()


@pytest.fixture
def test_user_data():
    """Test user registration data"""
    return {
        "email": "test@example.com",
        "password": "TestPass123",
        "company_name": "Test Company",
        "company_size": "10-50",
        "language": "fr",
        "country": "FR",
        "currency": "EUR",
        "timezone": "Europe/Paris"
    }


@pytest_asyncio.fixture
async def test_user(db_session: AsyncSession, test_user_data) -> User:
    """Create a test user in database"""
    from app.services.auth_service import AuthService
    from app.schemas.user import UserCreate
    
    user_create = UserCreate(**test_user_data)
    user = await AuthService.register_user(db_session, user_create)
    await db_session.commit()
    await db_session.refresh(user)
    
    return user


@pytest_asyncio.fixture
async def auth_headers(test_user: User) -> dict:
    """Get auth headers with access token for test user"""
    from app.services.auth_service import AuthService
    
    tokens = AuthService.create_tokens(test_user)
    
    return {
        "Authorization": f"Bearer {tokens.access_token}"
    }

