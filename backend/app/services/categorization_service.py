"""Transaction categorization service using AI"""
from typing import List
from sqlalchemy.ext.asyncio import AsyncSession
from uuid import UUID
from decimal import Decimal
import logging

from app.models.transaction import Transaction
from app.integrations.claude_client import ClaudeClient
from app.services.transaction_service import TransactionService

logger = logging.getLogger(__name__)


class CategorizationService:
    """Service for AI-powered transaction categorization"""
    
    @staticmethod
    async def categorize_transaction(
        db: AsyncSession,
        transaction: Transaction,
        ai_client: ClaudeClient = None
    ) -> Transaction:
        """
        Categorize a single transaction using AI.
        
        Args:
            db: Database session
            transaction: Transaction to categorize
            ai_client: Claude AI client (optional)
            
        Returns:
            Updated transaction with category
        """
        if ai_client is None:
            ai_client = ClaudeClient()
        
        try:
            category, confidence = await ai_client.categorize_transaction(
                description=transaction.description,
                amount=transaction.amount,
                transaction_type=transaction.transaction_type or "debit"
            )
            
            # Update transaction
            transaction.category = category
            transaction.category_confidence = confidence
            await db.flush()
            
            logger.info(
                f"Transaction {transaction.id} categorized as '{category}' "
                f"(confidence: {confidence})"
            )
            
            return transaction
            
        except Exception as e:
            logger.error(f"Failed to categorize transaction {transaction.id}: {e}")
            transaction.category = "autre"
            transaction.category_confidence = Decimal("0.0")
            await db.flush()
            return transaction
    
    @staticmethod
    async def categorize_uncategorized_transactions(
        db: AsyncSession,
        user_id: UUID,
        limit: int = 50,
        ai_client: ClaudeClient = None
    ) -> int:
        """
        Categorize all uncategorized transactions for a user.
        
        Args:
            db: Database session
            user_id: User ID
            limit: Max number of transactions to categorize
            ai_client: Claude AI client
            
        Returns:
            Number of transactions categorized
        """
        if ai_client is None:
            ai_client = ClaudeClient()
        
        # Get uncategorized transactions
        transactions = await TransactionService.get_uncategorized_transactions(
            db,
            user_id,
            limit
        )
        
        if not transactions:
            return 0
        
        # Categorize each transaction
        count = 0
        for transaction in transactions:
            try:
                await CategorizationService.categorize_transaction(
                    db,
                    transaction,
                    ai_client
                )
                count += 1
            except Exception as e:
                logger.error(f"Failed to categorize transaction {transaction.id}: {e}")
        
        await db.commit()
        
        logger.info(f"Categorized {count}/{len(transactions)} transactions for user {user_id}")
        return count
    
    @staticmethod
    async def get_category_breakdown(
        db: AsyncSession,
        user_id: UUID
    ) -> dict:
        """
        Get spending breakdown by category for user.
        
        Args:
            db: Database session
            user_id: User ID
            
        Returns:
            Dict of category → total amount
        """
        from sqlalchemy import func, select
        from app.models.bank_account import BankAccount
        
        result = await db.execute(
            select(
                Transaction.category,
                func.sum(Transaction.amount).label("total")
            )
            .join(BankAccount)
            .where(
                and_(
                    BankAccount.user_id == user_id,
                    Transaction.category.is_not(None),
                    Transaction.deleted_at.is_(None)
                )
            )
            .group_by(Transaction.category)
        )
        
        breakdown = {}
        for row in result:
            breakdown[row.category] = float(row.total)
        
        return breakdown
    
    @staticmethod
    async def recategorize_transaction(
        db: AsyncSession,
        transaction: Transaction,
        new_category: str,
        confidence: Decimal = Decimal("1.0")
    ) -> Transaction:
        """
        Manually recategorize a transaction.
        
        Args:
            db: Database session
            transaction: Transaction
            new_category: New category
            confidence: Confidence score (1.0 for manual)
            
        Returns:
            Updated transaction
        """
        transaction.category = new_category
        transaction.category_confidence = confidence
        await db.flush()
        
        logger.info(
            f"Transaction {transaction.id} manually recategorized to '{new_category}'"
        )
        
        return transaction


