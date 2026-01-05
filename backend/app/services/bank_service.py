"""Bank Account service - Business logic"""
from typing import Optional, List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_
from uuid import UUID
import logging

from app.models.bank_account import BankAccount
from app.models.user import User
from app.schemas.bank import BankAccountCreate, BankAccountUpdate

logger = logging.getLogger(__name__)


class BankService:
    """Bank account service"""
    
    @staticmethod
    async def create_bank_account(
        db: AsyncSession,
        user_id: UUID,
        account_data: BankAccountCreate
    ) -> BankAccount:
        """
        Create a new bank account.
        
        Args:
            db: Database session
            user_id: User ID
            account_data: Bank account creation data
            
        Returns:
            Created bank account
        """
        account = BankAccount(
            user_id=user_id,
            bank_name=account_data.bank_name,
            account_type=account_data.account_type,
            iban=account_data.iban,
            balance=account_data.balance,
            currency=account_data.currency,
            is_active=True,
        )
        
        db.add(account)
        await db.flush()
        
        logger.info(f"Bank account created: {account.id} for user {user_id}")
        return account
    
    @staticmethod
    async def get_bank_account(
        db: AsyncSession,
        account_id: UUID,
        user_id: UUID
    ) -> Optional[BankAccount]:
        """
        Get a bank account by ID (with ownership check).
        
        Args:
            db: Database session
            account_id: Account ID
            user_id: User ID (for ownership check)
            
        Returns:
            Bank account if found and owned by user, None otherwise
        """
        result = await db.execute(
            select(BankAccount).where(
                and_(
                    BankAccount.id == account_id,
                    BankAccount.user_id == user_id,
                    BankAccount.deleted_at.is_(None)
                )
            )
        )
        return result.scalar_one_or_none()
    
    @staticmethod
    async def get_user_bank_accounts(
        db: AsyncSession,
        user_id: UUID,
        is_active: Optional[bool] = None
    ) -> List[BankAccount]:
        """
        Get all bank accounts for a user.
        
        Args:
            db: Database session
            user_id: User ID
            is_active: Filter by active status (optional)
            
        Returns:
            List of bank accounts
        """
        conditions = [
            BankAccount.user_id == user_id,
            BankAccount.deleted_at.is_(None)
        ]
        
        if is_active is not None:
            conditions.append(BankAccount.is_active == is_active)
        
        result = await db.execute(
            select(BankAccount)
            .where(and_(*conditions))
            .order_by(BankAccount.created_at.desc())
        )
        return list(result.scalars().all())
    
    @staticmethod
    async def update_bank_account(
        db: AsyncSession,
        account: BankAccount,
        update_data: BankAccountUpdate
    ) -> BankAccount:
        """
        Update a bank account.
        
        Args:
            db: Database session
            account: Bank account to update
            update_data: Update data
            
        Returns:
            Updated bank account
        """
        update_dict = update_data.model_dump(exclude_unset=True)
        
        for field, value in update_dict.items():
            setattr(account, field, value)
        
        await db.flush()
        
        logger.info(f"Bank account updated: {account.id}")
        return account
    
    @staticmethod
    async def delete_bank_account(
        db: AsyncSession,
        account: BankAccount
    ) -> None:
        """
        Soft delete a bank account.
        
        Args:
            db: Database session
            account: Bank account to delete
        """
        from datetime import datetime
        account.deleted_at = datetime.utcnow()
        account.is_active = False
        await db.flush()
        
        logger.info(f"Bank account deleted: {account.id}")


