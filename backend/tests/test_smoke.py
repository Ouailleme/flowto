"""
Smoke tests to verify basic app functionality.
"""
import pytest


def test_app_imports():
    """Smoke test: verify app can be imported."""
    from app.main import app
    assert app is not None
    assert app.title == "FinanceAI"


def test_database_imports():
    """Smoke test: verify database can be imported."""
    from app.core.database import Base, engine, get_db
    assert Base is not None
    assert engine is not None
    assert get_db is not None


def test_models_import():
    """Smoke test: verify all models can be imported."""
    from app.models import (
        User,
        BankAccount,
        Transaction,
        Invoice,
        Reconciliation,
        Reminder,
        AuditLog,
    )
    assert User is not None
    assert BankAccount is not None
    assert Transaction is not None
    assert Invoice is not None
    assert Reconciliation is not None
    assert Reminder is not None
    assert AuditLog is not None


def test_services_import():
    """Smoke test: verify all services can be imported."""
    from app.services.auth_service import AuthService
    from app.services.bank_service import BankService
    from app.services.invoice_service import InvoiceService
    from app.services.transaction_service import TransactionService
    from app.services.reconciliation_service import ReconciliationService
    from app.services.reminder_service import ReminderService
    
    assert AuthService is not None
    assert BankService is not None
    assert InvoiceService is not None
    assert TransactionService is not None
    assert ReconciliationService is not None
    assert ReminderService is not None


@pytest.mark.asyncio
async def test_database_connection(db_session):
    """Test that we can connect to the test database."""
    from sqlalchemy import text
    result = await db_session.execute(text("SELECT 1"))
    assert result.scalar() == 1


@pytest.mark.asyncio
async def test_create_test_user(test_user):
    """Test that test_user fixture creates a user."""
    assert test_user.id is not None
    assert test_user.email == "test@example.com"
    assert test_user.is_verified is True


@pytest.mark.asyncio
async def test_auth_headers(auth_headers):
    """Test that auth_headers fixture provides valid headers."""
    assert "Authorization" in auth_headers
    assert auth_headers["Authorization"].startswith("Bearer ")

