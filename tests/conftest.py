"""Pytest configuration and fixtures"""
import pytest
import asyncio
from typing import AsyncGenerator, Generator
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.pool import NullPool
from httpx import AsyncClient, ASGITransport
from uuid import uuid4

from app.core.database import Base, get_db
from app.main import app
from app.models.user import User
from app.core.security import hash_password, create_access_token
from app.config import settings

# Test database URL
TEST_DATABASE_URL = "postgresql+asyncpg://postgres:postgres@localhost:5432/financeai_test"

# Create test engine
test_engine = create_async_engine(
    TEST_DATABASE_URL,
    poolclass=NullPool,
    echo=False,
)

TestSessionLocal = async_sessionmaker(
    test_engine,
    class_=AsyncSession,
    expire_on_commit=False,
)


@pytest.fixture(scope="session")
def event_loop() -> Generator:
    """Create event loop for async tests"""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope="function", autouse=True)
async def setup_database():
    """Setup and teardown database for each test"""
    # Create all tables
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    
    yield
    
    # Drop all tables
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


@pytest.fixture
async def db_session() -> AsyncGenerator[AsyncSession, None]:
    """Get test database session"""
    async with TestSessionLocal() as session:
        yield session


@pytest.fixture
async def test_user(db_session: AsyncSession) -> User:
    """Create a test user"""
    user = User(
        email="test@example.com",
        hashed_password=hash_password("testpassword123"),
        is_active=True,
        language="fr",
        country="FR",
        currency="EUR",
        timezone="Europe/Paris",
        locale="fr_FR",
    )
    db_session.add(user)
    await db_session.commit()
    await db_session.refresh(user)
    return user


@pytest.fixture
async def test_user_2(db_session: AsyncSession) -> User:
    """Create a second test user"""
    user = User(
        email="test2@example.com",
        hashed_password=hash_password("testpassword123"),
        is_active=True,
        language="en",
        country="GB",
        currency="GBP",
        timezone="Europe/London",
        locale="en_GB",
    )
    db_session.add(user)
    await db_session.commit()
    await db_session.refresh(user)
    return user


@pytest.fixture
def auth_token(test_user: User) -> str:
    """Create JWT token for test user"""
    return create_access_token(subject=str(test_user.id))


@pytest.fixture
def auth_headers(auth_token: str) -> dict:
    """Create auth headers with JWT token"""
    return {"Authorization": f"Bearer {auth_token}"}


@pytest.fixture
async def client(db_session: AsyncSession) -> AsyncGenerator[AsyncClient, None]:
    """Create test client with database override"""
    
    async def override_get_db():
        yield db_session
    
    app.dependency_overrides[get_db] = override_get_db
    
    async with AsyncClient(
        transport=ASGITransport(app=app),
        base_url="http://test"
    ) as ac:
        yield ac
    
    app.dependency_overrides.clear()


# Factories for test data
from datetime import date, datetime, timedelta
from decimal import Decimal


@pytest.fixture
def invoice_factory():
    """Factory for creating test invoice data"""
    def _factory(**kwargs):
        defaults = {
            "invoice_number": f"INV-TEST-{uuid4().hex[:8]}",
            "client_name": "Test Client",
            "client_email": "client@test.com",
            "amount": Decimal("1000.00"),
            "tax_amount": Decimal("200.00"),
            "currency": "EUR",
            "issue_date": date.today(),
            "due_date": date.today() + timedelta(days=30),
            "description": "Test invoice",
        }
        defaults.update(kwargs)
        return defaults
    return _factory


@pytest.fixture
def bank_account_factory():
    """Factory for creating test bank account data"""
    def _factory(**kwargs):
        defaults = {
            "bank_name": "Test Bank",
            "account_type": "checking",
            "iban": f"FR76{uuid4().hex[:20].upper()}",
            "balance": Decimal("5000.00"),
            "currency": "EUR",
        }
        defaults.update(kwargs)
        return defaults
    return _factory


@pytest.fixture
def transaction_factory():
    """Factory for creating test transaction data"""
    def _factory(**kwargs):
        defaults = {
            "date": datetime.utcnow(),
            "description": "Test transaction",
            "amount": Decimal("-100.00"),
            "currency": "EUR",
            "transaction_type": "debit",
        }
        defaults.update(kwargs)
        return defaults
    return _factory


