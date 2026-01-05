"""Unit tests for BankService"""
import pytest
from uuid import uuid4
from decimal import Decimal

from app.services.bank_service import BankService
from app.schemas.bank import BankAccountCreate, BankAccountUpdate
from app.models.bank_account import BankAccount


@pytest.mark.asyncio
class TestBankService:
    """Test BankService"""
    
    async def test_create_bank_account(
        self,
        db_session,
        test_user,
        bank_account_factory
    ):
        """Test creating a bank account"""
        data = BankAccountCreate(**bank_account_factory())
        
        account = await BankService.create_bank_account(
            db_session,
            test_user.id,
            data
        )
        
        assert account.id is not None
        assert account.user_id == test_user.id
        assert account.bank_name == data.bank_name
        assert account.balance == data.balance
        assert account.currency == data.currency
        assert account.is_active is True
    
    async def test_get_bank_account(
        self,
        db_session,
        test_user,
        bank_account_factory
    ):
        """Test getting a bank account by ID"""
        # Create account
        data = BankAccountCreate(**bank_account_factory())
        account = await BankService.create_bank_account(
            db_session,
            test_user.id,
            data
        )
        await db_session.commit()
        
        # Get account
        retrieved = await BankService.get_bank_account(
            db_session,
            account.id,
            test_user.id
        )
        
        assert retrieved is not None
        assert retrieved.id == account.id
        assert retrieved.bank_name == account.bank_name
    
    async def test_get_bank_account_wrong_user(
        self,
        db_session,
        test_user,
        test_user_2,
        bank_account_factory
    ):
        """Test that user cannot access another user's account"""
        # Create account for user 1
        data = BankAccountCreate(**bank_account_factory())
        account = await BankService.create_bank_account(
            db_session,
            test_user.id,
            data
        )
        await db_session.commit()
        
        # Try to get account as user 2
        retrieved = await BankService.get_bank_account(
            db_session,
            account.id,
            test_user_2.id
        )
        
        assert retrieved is None
    
    async def test_get_user_bank_accounts(
        self,
        db_session,
        test_user,
        bank_account_factory
    ):
        """Test getting all bank accounts for a user"""
        # Create 3 accounts
        for i in range(3):
            data = BankAccountCreate(**bank_account_factory(
                bank_name=f"Bank {i}"
            ))
            await BankService.create_bank_account(
                db_session,
                test_user.id,
                data
            )
        await db_session.commit()
        
        # Get all accounts
        accounts = await BankService.get_user_bank_accounts(
            db_session,
            test_user.id
        )
        
        assert len(accounts) == 3
        assert all(acc.user_id == test_user.id for acc in accounts)
    
    async def test_get_user_bank_accounts_filtered_active(
        self,
        db_session,
        test_user,
        bank_account_factory
    ):
        """Test filtering bank accounts by active status"""
        # Create 2 active and 1 inactive
        for i in range(2):
            data = BankAccountCreate(**bank_account_factory())
            await BankService.create_bank_account(
                db_session,
                test_user.id,
                data
            )
        
        # Create inactive
        data = BankAccountCreate(**bank_account_factory())
        account = await BankService.create_bank_account(
            db_session,
            test_user.id,
            data
        )
        account.is_active = False
        await db_session.commit()
        
        # Get only active
        active_accounts = await BankService.get_user_bank_accounts(
            db_session,
            test_user.id,
            is_active=True
        )
        
        assert len(active_accounts) == 2
        assert all(acc.is_active for acc in active_accounts)
    
    async def test_update_bank_account(
        self,
        db_session,
        test_user,
        bank_account_factory
    ):
        """Test updating a bank account"""
        # Create account
        data = BankAccountCreate(**bank_account_factory(
            balance=Decimal("1000.00")
        ))
        account = await BankService.create_bank_account(
            db_session,
            test_user.id,
            data
        )
        await db_session.commit()
        
        # Update account
        update_data = BankAccountUpdate(
            balance=Decimal("2000.00"),
            is_active=False
        )
        updated = await BankService.update_bank_account(
            db_session,
            account,
            update_data
        )
        await db_session.commit()
        
        assert updated.balance == Decimal("2000.00")
        assert updated.is_active is False
    
    async def test_delete_bank_account(
        self,
        db_session,
        test_user,
        bank_account_factory
    ):
        """Test soft deleting a bank account"""
        # Create account
        data = BankAccountCreate(**bank_account_factory())
        account = await BankService.create_bank_account(
            db_session,
            test_user.id,
            data
        )
        await db_session.commit()
        
        # Delete account
        await BankService.delete_bank_account(db_session, account)
        await db_session.commit()
        
        # Verify soft delete
        assert account.deleted_at is not None
        assert account.is_active is False
        
        # Verify cannot retrieve
        retrieved = await BankService.get_bank_account(
            db_session,
            account.id,
            test_user.id
        )
        assert retrieved is None


