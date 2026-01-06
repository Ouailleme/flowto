"""Tests for BankService"""
import pytest
from datetime import datetime, timedelta
from decimal import Decimal
from uuid import uuid4
from unittest.mock import AsyncMock, MagicMock, patch

from app.services.bank_service import BankService
from app.models.bank_account import BankAccount
from app.models.transaction import Transaction
from app.schemas.bank import BankAccountCreate, BankAccountUpdate
from app.integrations.bridge_client import BridgeClient, BridgeAPIError


@pytest.fixture
def sample_bank_account_data():
    """Sample bank account data"""
    return BankAccountCreate(
        bank_name="Test Bank",
        account_type="checking",
        iban="FR1420041010050500013M02606",
        balance=Decimal("1000.00"),
        currency="EUR"
    )


@pytest.fixture
def sample_bridge_account_data():
    """Sample Bridge API account data"""
    return {
        "id": 123456,
        "bank_name": "BNP Paribas",
        "type": "checking",
        "iban": "FR7630001007941234567890185",
        "balance": 2500.50,
        "currency_code": "EUR",
        "item_id": 789,
        "updated_at": "2024-01-01T12:00:00Z"
    }


@pytest.fixture
def sample_bridge_transactions():
    """Sample Bridge API transactions"""
    return [
        {
            "id": 1001,
            "clean_description": "Payment Salary",
            "raw_description": "VIR SEPA SALARY",
            "amount": 3000.00,
            "currency_code": "EUR",
            "date": "2024-01-15T00:00:00Z",
        },
        {
            "id": 1002,
            "clean_description": "Supermarket",
            "raw_description": "CARTE 01/14 CARREFOUR",
            "amount": -85.50,
            "currency_code": "EUR",
            "date": "2024-01-14T00:00:00Z",
        }
    ]


@pytest.mark.asyncio
async def test_create_bank_account(db_session, test_user, sample_bank_account_data):
    """Test creating a bank account"""
    account = await BankService.create_bank_account(
        db=db_session,
        user_id=test_user.id,
        account_data=sample_bank_account_data
    )
    
    assert account.id is not None
    assert account.user_id == test_user.id
    assert account.bank_name == sample_bank_account_data.bank_name
    assert account.account_type == sample_bank_account_data.account_type
    assert account.iban == sample_bank_account_data.iban
    assert account.balance == sample_bank_account_data.balance
    assert account.currency == sample_bank_account_data.currency
    assert account.is_active is True


@pytest.mark.asyncio
async def test_get_bank_account(db_session, test_user):
    """Test getting a bank account"""
    # Create account
    account_data = BankAccountCreate(
        bank_name="Test Bank",
        account_type="checking",
        balance=Decimal("500.00"),
        currency="EUR"
    )
    
    created_account = await BankService.create_bank_account(
        db=db_session,
        user_id=test_user.id,
        account_data=account_data
    )
    await db_session.commit()
    
    # Get account
    retrieved_account = await BankService.get_bank_account(
        db=db_session,
        account_id=created_account.id,
        user_id=test_user.id
    )
    
    assert retrieved_account is not None
    assert retrieved_account.id == created_account.id
    assert retrieved_account.bank_name == "Test Bank"


@pytest.mark.asyncio
async def test_get_bank_account_wrong_user(db_session, test_user):
    """Test getting account with wrong user returns None"""
    account_data = BankAccountCreate(
        bank_name="Test Bank",
        account_type="checking",
        balance=Decimal("500.00"),
        currency="EUR"
    )
    
    created_account = await BankService.create_bank_account(
        db=db_session,
        user_id=test_user.id,
        account_data=account_data
    )
    await db_session.commit()
    
    # Try to get with different user ID
    wrong_user_id = uuid4()
    retrieved_account = await BankService.get_bank_account(
        db=db_session,
        account_id=created_account.id,
        user_id=wrong_user_id
    )
    
    assert retrieved_account is None


@pytest.mark.asyncio
async def test_get_user_bank_accounts(db_session, test_user):
    """Test getting all bank accounts for a user"""
    # Create multiple accounts
    for i in range(3):
        account_data = BankAccountCreate(
            bank_name=f"Bank {i}",
            account_type="checking",
            balance=Decimal("1000.00"),
            currency="EUR"
        )
        await BankService.create_bank_account(
            db=db_session,
            user_id=test_user.id,
            account_data=account_data
        )
    await db_session.commit()
    
    # Get all accounts
    accounts = await BankService.get_user_bank_accounts(
        db=db_session,
        user_id=test_user.id
    )
    
    assert len(accounts) == 3


@pytest.mark.asyncio
async def test_get_user_bank_accounts_filter_active(db_session, test_user):
    """Test filtering bank accounts by active status"""
    # Create active and inactive accounts
    active_data = BankAccountCreate(
        bank_name="Active Bank",
        account_type="checking",
        balance=Decimal("1000.00"),
        currency="EUR"
    )
    active_account = await BankService.create_bank_account(
        db=db_session,
        user_id=test_user.id,
        account_data=active_data
    )
    
    inactive_data = BankAccountCreate(
        bank_name="Inactive Bank",
        account_type="checking",
        balance=Decimal("500.00"),
        currency="EUR"
    )
    inactive_account = await BankService.create_bank_account(
        db=db_session,
        user_id=test_user.id,
        account_data=inactive_data
    )
    inactive_account.is_active = False
    await db_session.commit()
    
    # Get only active accounts
    active_accounts = await BankService.get_user_bank_accounts(
        db=db_session,
        user_id=test_user.id,
        is_active=True
    )
    
    assert len(active_accounts) == 1
    assert active_accounts[0].bank_name == "Active Bank"


@pytest.mark.asyncio
async def test_update_bank_account(db_session, test_user):
    """Test updating a bank account"""
    account_data = BankAccountCreate(
        bank_name="Original Bank",
        account_type="checking",
        balance=Decimal("1000.00"),
        currency="EUR"
    )
    
    account = await BankService.create_bank_account(
        db=db_session,
        user_id=test_user.id,
        account_data=account_data
    )
    await db_session.commit()
    
    # Update account
    update_data = BankAccountUpdate(
        bank_name="Updated Bank",
        balance=Decimal("1500.00")
    )
    
    updated_account = await BankService.update_bank_account(
        db=db_session,
        account=account,
        update_data=update_data
    )
    await db_session.commit()
    
    assert updated_account.bank_name == "Updated Bank"
    assert updated_account.balance == Decimal("1500.00")


@pytest.mark.asyncio
async def test_delete_bank_account(db_session, test_user):
    """Test soft deleting a bank account"""
    account_data = BankAccountCreate(
        bank_name="Test Bank",
        account_type="checking",
        balance=Decimal("1000.00"),
        currency="EUR"
    )
    
    account = await BankService.create_bank_account(
        db=db_session,
        user_id=test_user.id,
        account_data=account_data
    )
    await db_session.commit()
    
    # Delete account
    await BankService.delete_bank_account(db=db_session, account=account)
    await db_session.commit()
    
    # Check account is soft deleted
    assert account.deleted_at is not None
    assert account.is_active is False
    
    # Verify it's not returned in regular queries
    accounts = await BankService.get_user_bank_accounts(
        db=db_session,
        user_id=test_user.id
    )
    assert len(accounts) == 0


@pytest.mark.asyncio
async def test_connect_bridge_account_new(db_session, test_user, sample_bridge_account_data):
    """Test connecting a new Bridge account"""
    bridge_user_uuid = "bridge-user-123"
    
    account = await BankService.connect_bridge_account(
        db=db_session,
        user_id=test_user.id,
        bridge_account_data=sample_bridge_account_data,
        bridge_user_uuid=bridge_user_uuid
    )
    
    assert account.id is not None
    assert account.user_id == test_user.id
    assert account.bank_name == "BNP Paribas"
    assert account.account_type == "checking"
    assert account.iban == "FR7630001007941234567890185"
    assert account.balance == Decimal("2500.50")
    assert account.currency == "EUR"
    assert account.bridge_account_id == "123456"
    assert account.bridge_user_uuid == bridge_user_uuid
    assert account.bridge_item_id == "789"
    assert account.is_active is True
    assert account.last_sync_at is not None


@pytest.mark.asyncio
async def test_connect_bridge_account_existing(db_session, test_user, sample_bridge_account_data):
    """Test connecting an existing Bridge account (update)"""
    bridge_user_uuid = "bridge-user-123"
    
    # Create initial account
    account1 = await BankService.connect_bridge_account(
        db=db_session,
        user_id=test_user.id,
        bridge_account_data=sample_bridge_account_data,
        bridge_user_uuid=bridge_user_uuid
    )
    await db_session.commit()
    initial_id = account1.id
    
    # Update with new balance
    updated_data = sample_bridge_account_data.copy()
    updated_data["balance"] = 3000.00
    
    account2 = await BankService.connect_bridge_account(
        db=db_session,
        user_id=test_user.id,
        bridge_account_data=updated_data,
        bridge_user_uuid=bridge_user_uuid
    )
    await db_session.commit()
    
    # Should return same account with updated balance
    assert account2.id == initial_id
    assert account2.balance == Decimal("3000.00")


@pytest.mark.asyncio
async def test_sync_transactions_success(db_session, test_user, sample_bridge_transactions):
    """Test syncing transactions from Bridge API"""
    # Create bank account
    account_data = BankAccountCreate(
        bank_name="Test Bank",
        account_type="checking",
        balance=Decimal("1000.00"),
        currency="EUR"
    )
    account = await BankService.create_bank_account(
        db=db_session,
        user_id=test_user.id,
        account_data=account_data
    )
    account.bridge_account_id = "123456"
    await db_session.commit()
    
    # Mock Bridge client
    mock_bridge_client = AsyncMock(spec=BridgeClient)
    mock_bridge_client.sync_account_transactions.return_value = sample_bridge_transactions
    mock_bridge_client.get_account_balance.return_value = {
        "balance": 2914.50,
        "currency": "EUR"
    }
    mock_bridge_client.format_transaction.side_effect = lambda tx: {
        "bridge_transaction_id": str(tx["id"]),
        "description": tx["clean_description"],
        "amount": tx["amount"],
        "currency": tx["currency_code"],
        "date": datetime.fromisoformat(tx["date"].replace("Z", "+00:00")),
        "transaction_type": "credit" if tx["amount"] > 0 else "debit",
        "raw_data": tx
    }
    
    # Sync transactions
    result = await BankService.sync_transactions(
        db=db_session,
        account=account,
        bridge_client=mock_bridge_client
    )
    
    assert result["new_count"] == 2
    assert result["updated_count"] == 0
    assert result["balance"] == 2914.50
    assert "last_sync" in result
    
    # Verify transactions were created
    assert mock_bridge_client.sync_account_transactions.called
    assert mock_bridge_client.get_account_balance.called


@pytest.mark.asyncio
async def test_sync_transactions_no_bridge_id(db_session, test_user):
    """Test syncing transactions fails without bridge_account_id"""
    account_data = BankAccountCreate(
        bank_name="Manual Bank",
        account_type="checking",
        balance=Decimal("1000.00"),
        currency="EUR"
    )
    account = await BankService.create_bank_account(
        db=db_session,
        user_id=test_user.id,
        account_data=account_data
    )
    # No bridge_account_id set
    
    mock_bridge_client = AsyncMock(spec=BridgeClient)
    
    with pytest.raises(ValueError, match="not connected to Bridge API"):
        await BankService.sync_transactions(
            db=db_session,
            account=account,
            bridge_client=mock_bridge_client
        )


@pytest.mark.asyncio
async def test_sync_transactions_bridge_error(db_session, test_user):
    """Test syncing transactions handles Bridge API errors"""
    account_data = BankAccountCreate(
        bank_name="Test Bank",
        account_type="checking",
        balance=Decimal("1000.00"),
        currency="EUR"
    )
    account = await BankService.create_bank_account(
        db=db_session,
        user_id=test_user.id,
        account_data=account_data
    )
    account.bridge_account_id = "123456"
    await db_session.commit()
    
    # Mock Bridge client to raise error
    mock_bridge_client = AsyncMock(spec=BridgeClient)
    mock_bridge_client.sync_account_transactions.side_effect = BridgeAPIError("API Error")
    
    with pytest.raises(ValueError, match="Failed to sync transactions"):
        await BankService.sync_transactions(
            db=db_session,
            account=account,
            bridge_client=mock_bridge_client
        )


@pytest.mark.asyncio
async def test_sync_transactions_updates_existing(db_session, test_user, sample_bridge_transactions):
    """Test syncing updates existing transactions"""
    # Create bank account
    account_data = BankAccountCreate(
        bank_name="Test Bank",
        account_type="checking",
        balance=Decimal("1000.00"),
        currency="EUR"
    )
    account = await BankService.create_bank_account(
        db=db_session,
        user_id=test_user.id,
        account_data=account_data
    )
    account.bridge_account_id = "123456"
    await db_session.commit()
    
    # Create existing transaction
    existing_tx = Transaction(
        user_id=test_user.id,
        bank_account_id=account.id,
        bridge_transaction_id="1001",
        description="Old Description",
        amount=Decimal("2500.00"),  # Different amount
        currency="EUR",
        date=datetime.utcnow(),
        transaction_type="credit"
    )
    db_session.add(existing_tx)
    await db_session.commit()
    
    # Mock Bridge client
    mock_bridge_client = AsyncMock(spec=BridgeClient)
    mock_bridge_client.sync_account_transactions.return_value = sample_bridge_transactions
    mock_bridge_client.get_account_balance.return_value = {
        "balance": 2914.50,
        "currency": "EUR"
    }
    mock_bridge_client.format_transaction.side_effect = lambda tx: {
        "bridge_transaction_id": str(tx["id"]),
        "description": tx["clean_description"],
        "amount": tx["amount"],
        "currency": tx["currency_code"],
        "date": datetime.fromisoformat(tx["date"].replace("Z", "+00:00")),
        "transaction_type": "credit" if tx["amount"] > 0 else "debit",
        "raw_data": tx
    }
    
    # Sync transactions
    result = await BankService.sync_transactions(
        db=db_session,
        account=account,
        bridge_client=mock_bridge_client
    )
    
    # One updated (1001), one new (1002)
    assert result["new_count"] == 1
    assert result["updated_count"] == 1

