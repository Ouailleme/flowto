"""
Pytest configuration and fixtures for FinanceAI tests.
"""
import asyncio
from typing import AsyncGenerator, Generator
import pytest
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy.pool import NullPool
from httpx import AsyncClient

from app.main import app
from app.core.database import Base, get_db
from app.models.user import User
from app.core.security import hash_password

# Test database URL (PostgreSQL test database)
# Note: We use PostgreSQL for tests to match production environment
# This avoids type compatibility issues (e.g., UUID type)
TEST_DATABASE_URL = "postgresql+asyncpg://financeai:financeai2026@postgres:5432/financeai_test"


@pytest.fixture(scope="session")
def event_loop() -> Generator:
    """
    Create an event loop for the test session.
    Required for async tests.
    """
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope="function")
async def test_engine():
    """
    Create a test database engine.
    Uses in-memory SQLite for speed.
    """
    engine = create_async_engine(
        TEST_DATABASE_URL,
        poolclass=NullPool,
        echo=False,
    )
    
    # Create all tables
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    
    yield engine
    
    # Drop all tables
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
    
    await engine.dispose()


@pytest.fixture(scope="function")
async def db_session(test_engine) -> AsyncGenerator[AsyncSession, None]:
    """
    Create a test database session.
    Each test gets a fresh session that is rolled back after the test.
    """
    async_session_maker = async_sessionmaker(
        test_engine,
        class_=AsyncSession,
        expire_on_commit=False,
    )
    
    async with async_session_maker() as session:
        yield session


@pytest.fixture(scope="function")
async def client(db_session: AsyncSession) -> AsyncGenerator[AsyncClient, None]:
    """
    Create a test HTTP client.
    Overrides the database dependency to use the test database.
    """
    async def override_get_db():
        yield db_session
    
    app.dependency_overrides[get_db] = override_get_db
    
    async with AsyncClient(app=app, base_url="http://test") as ac:
        yield ac
    
    app.dependency_overrides.clear()


@pytest.fixture
async def test_user(db_session: AsyncSession) -> User:
    """
    Create a test user in the database.
    
    Credentials:
    - Email: test@example.com
    - Password: TestPassword123!
    """
    user = User(
        email="test@example.com",
        hashed_password=hash_password("TestPassword123!"),
        full_name="Test User",
        company_name="Test Company",
        is_active=True,
        is_verified=True,
    )
    db_session.add(user)
    await db_session.commit()
    await db_session.refresh(user)
    return user


@pytest.fixture
async def test_user_unverified(db_session: AsyncSession) -> User:
    """
    Create an unverified test user.
    
    Credentials:
    - Email: unverified@example.com
    - Password: TestPassword123!
    """
    user = User(
        email="unverified@example.com",
        hashed_password=hash_password("TestPassword123!"),
        full_name="Unverified User",
        company_name="Unverified Company",
        is_active=True,
        is_verified=False,
    )
    db_session.add(user)
    await db_session.commit()
    await db_session.refresh(user)
    return user


@pytest.fixture
async def auth_headers(client: AsyncClient, test_user: User) -> dict:
    """
    Get authentication headers for a test user.
    Returns a dict with Authorization header.
    """
    # Login to get access token
    response = await client.post(
        "/api/v1/auth/login",
        json={
            "email": "test@example.com",
            "password": "TestPassword123!",
        },
    )
    assert response.status_code == 200
    data = response.json()
    access_token = data["access_token"]
    
    return {"Authorization": f"Bearer {access_token}"}
