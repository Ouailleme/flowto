"""Transaction service - Business logic"""
from typing import Optional, List, Tuple
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_, or_, func
from uuid import UUID
from datetime import datetime
from decimal import Decimal
import logging

from app.models.transaction import Transaction
from app.schemas.transaction import TransactionCreate, TransactionUpdate, TransactionFilter

logger = logging.getLogger(__name__)


class TransactionService:
    """Transaction service"""
    
    @staticmethod
    async def create_transaction(
        db: AsyncSession,
        transaction_data: TransactionCreate
    ) -> Transaction:
        """Create a new transaction"""
        # Calculate total amount with currency
        total = transaction_data.amount
        
        transaction = Transaction(
            bank_account_id=transaction_data.bank_account_id,
            date=transaction_data.date,
            description=transaction_data.description,
            amount=transaction_data.amount,
            currency=transaction_data.currency,
            transaction_type=transaction_data.transaction_type,
            bridge_transaction_id=transaction_data.bridge_transaction_id,
            external_id=transaction_data.external_id,
            is_reconciled=False,
        )
        
        db.add(transaction)
        await db.flush()
        
        logger.info(f"Transaction created: {transaction.id}")
        return transaction
    
    @staticmethod
    async def get_transaction(
        db: AsyncSession,
        transaction_id: UUID,
        user_id: UUID
    ) -> Optional[Transaction]:
        """
        Get transaction by ID with ownership check.
        
        Joins with bank_account to check user ownership.
        """
        from app.models.bank_account import BankAccount
        
        result = await db.execute(
            select(Transaction)
            .join(BankAccount)
            .where(
                and_(
                    Transaction.id == transaction_id,
                    BankAccount.user_id == user_id,
                    Transaction.deleted_at.is_(None)
                )
            )
        )
        return result.scalar_one_or_none()
    
    @staticmethod
    async def get_transactions(
        db: AsyncSession,
        user_id: UUID,
        filters: TransactionFilter,
        page: int = 1,
        page_size: int = 50
    ) -> Tuple[List[Transaction], int]:
        """
        Get transactions with filters and pagination.
        
        Returns:
            Tuple of (transactions list, total count)
        """
        from app.models.bank_account import BankAccount
        
        # Base query
        query = select(Transaction).join(BankAccount).where(
            and_(
                BankAccount.user_id == user_id,
                Transaction.deleted_at.is_(None)
            )
        )
        
        # Apply filters
        conditions = []
        
        if filters.bank_account_id:
            conditions.append(Transaction.bank_account_id == filters.bank_account_id)
        
        if filters.start_date:
            conditions.append(Transaction.date >= filters.start_date)
        
        if filters.end_date:
            conditions.append(Transaction.date <= filters.end_date)
        
        if filters.category:
            conditions.append(Transaction.category == filters.category)
        
        if filters.is_reconciled is not None:
            conditions.append(Transaction.is_reconciled == filters.is_reconciled)
        
        if filters.min_amount is not None:
            conditions.append(Transaction.amount >= filters.min_amount)
        
        if filters.max_amount is not None:
            conditions.append(Transaction.amount <= filters.max_amount)
        
        if filters.search:
            conditions.append(
                Transaction.description.ilike(f"%{filters.search}%")
            )
        
        if conditions:
            query = query.where(and_(*conditions))
        
        # Count total
        count_query = select(func.count()).select_from(query.subquery())
        total_result = await db.execute(count_query)
        total = total_result.scalar() or 0
        
        # Apply pagination
        query = query.order_by(Transaction.date.desc())
        query = query.offset((page - 1) * page_size).limit(page_size)
        
        result = await db.execute(query)
        transactions = list(result.scalars().all())
        
        return transactions, total
    
    @staticmethod
    async def update_transaction(
        db: AsyncSession,
        transaction: Transaction,
        update_data: TransactionUpdate
    ) -> Transaction:
        """Update transaction"""
        update_dict = update_data.model_dump(exclude_unset=True)
        
        for field, value in update_dict.items():
            setattr(transaction, field, value)
        
        await db.flush()
        
        logger.info(f"Transaction updated: {transaction.id}")
        return transaction
    
    @staticmethod
    async def categorize_transaction(
        db: AsyncSession,
        transaction: Transaction,
        category: str,
        confidence: Decimal
    ) -> Transaction:
        """Set AI category for transaction"""
        transaction.category = category
        transaction.category_confidence = confidence
        await db.flush()
        
        logger.info(f"Transaction categorized: {transaction.id} → {category}")
        return transaction
    
    @staticmethod
    async def get_uncategorized_transactions(
        db: AsyncSession,
        user_id: UUID,
        limit: int = 100
    ) -> List[Transaction]:
        """Get transactions without AI category"""
        from app.models.bank_account import BankAccount
        
        result = await db.execute(
            select(Transaction)
            .join(BankAccount)
            .where(
                and_(
                    BankAccount.user_id == user_id,
                    Transaction.category.is_(None),
                    Transaction.deleted_at.is_(None)
                )
            )
            .order_by(Transaction.date.desc())
            .limit(limit)
        )
        return list(result.scalars().all())


