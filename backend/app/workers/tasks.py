"""Celery tasks for background processing"""
from celery import Task
from celery.utils.log import get_task_logger
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
import asyncio
from typing import Optional

from app.config import settings
from app.workers.celery_app import celery_app
from app.integrations.bridge_client import BridgeClient, BridgeAPIError
from app.integrations.claude_client import ClaudeClient
from app.integrations.sendgrid_client import SendGridClient
from app.services.categorization_service import CategorizationService
from app.services.reconciliation_service import ReconciliationService
from app.services.reminder_service import ReminderService

logger = get_task_logger(__name__)


# Database session for tasks
engine = create_async_engine(
    settings.DATABASE_URL,
    pool_pre_ping=True,
    echo=False,
)

SessionLocal = async_sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False,
)


class AsyncTask(Task):
    """Base task class for async operations"""
    
    def __call__(self, *args, **kwargs):
        """Run async task in event loop"""
        return asyncio.run(self.run_async(*args, **kwargs))
    
    async def run_async(self, *args, **kwargs):
        """Override this method in subclasses"""
        raise NotImplementedError


@celery_app.task(
    bind=True,
    base=AsyncTask,
    max_retries=3,
    time_limit=300,
    soft_time_limit=270
)
async def categorize_uncategorized_transactions_task(self, user_id: Optional[str] = None):
    """
    Categorize all uncategorized transactions.
    
    Args:
        user_id: Optional user ID (if None, process all users)
    """
    try:
        async with SessionLocal() as db:
            ai_client = ClaudeClient()
            
            if user_id:
                from uuid import UUID
                user_uuid = UUID(user_id)
                count = await CategorizationService.categorize_uncategorized_transactions(
                    db,
                    user_uuid,
                    limit=50,
                    ai_client=ai_client
                )
                logger.info(f"Categorized {count} transactions for user {user_id}")
            else:
                # TODO: Process all users
                logger.info("Processing all users not yet implemented")
                count = 0
            
            return {"categorized": count}
            
    except Exception as e:
        logger.error(f"Failed to categorize transactions: {e}")
        raise self.retry(exc=e, countdown=60 * (2 ** self.request.retries))


@celery_app.task(
    bind=True,
    base=AsyncTask,
    max_retries=3,
    time_limit=600,
    soft_time_limit=540
)
async def process_overdue_invoices_task(self, user_id: Optional[str] = None):
    """
    Process overdue invoices and send reminders.
    
    Args:
        user_id: Optional user ID (if None, process all users)
    """
    try:
        async with SessionLocal() as db:
            ai_client = ClaudeClient()
            email_client = SendGridClient()
            
            if user_id:
                from uuid import UUID
                user_uuid = UUID(user_id)
                stats = await ReminderService.process_overdue_invoices(
                    db,
                    user_uuid,
                    ai_client,
                    email_client
                )
                logger.info(
                    f"Processed {stats['total']} overdue invoices for user {user_id}: "
                    f"{stats['sent']} sent, {stats['failed']} failed"
                )
            else:
                # TODO: Process all users
                logger.info("Processing all users not yet implemented")
                stats = {"total": 0, "sent": 0, "failed": 0}
            
            return stats
            
    except Exception as e:
        logger.error(f"Failed to process overdue invoices: {e}")
        raise self.retry(exc=e, countdown=120 * (2 ** self.request.retries))


@celery_app.task(
    bind=True,
    base=AsyncTask,
    max_retries=3,
    time_limit=1800,  # 30 minutes
    soft_time_limit=1620
)
async def sync_bank_account_task(self, bank_account_id: str):
    """
    Sync transactions for a bank account from Bridge API.
    
    Args:
        bank_account_id: Bank account UUID
    """
    try:
        async with SessionLocal() as db:
            from uuid import UUID
            from app.models.bank_account import BankAccount
            from app.schemas.transaction import TransactionCreate
            from app.services.transaction_service import TransactionService
            from datetime import datetime, timedelta
            
            account_uuid = UUID(bank_account_id)
            
            # Get bank account
            bank_account = await db.get(BankAccount, account_uuid)
            if not bank_account:
                logger.error(f"Bank account {bank_account_id} not found")
                return {"error": "Bank account not found"}
            
            if not bank_account.bridge_account_id:
                logger.warning(f"Bank account {bank_account_id} has no Bridge ID")
                return {"error": "No Bridge account ID"}
            
            # Fetch transactions from Bridge
            bridge_client = BridgeClient()
            
            last_sync = bank_account.last_sync_at or datetime.utcnow() - timedelta(days=90)
            
            try:
                raw_transactions = await bridge_client.get_transactions(
                    account_id=int(bank_account.bridge_account_id),
                    since=last_sync
                )
                
                # Save transactions
                new_count = 0
                for raw_tx in raw_transactions:
                    formatted = bridge_client.format_transaction(raw_tx)
                    
                    # Check if already exists
                    from sqlalchemy import select
                    existing = await db.execute(
                        select(Transaction).where(
                            Transaction.bridge_transaction_id == formatted["bridge_transaction_id"]
                        )
                    )
                    
                    if existing.scalar_one_or_none():
                        continue
                    
                    # Create transaction
                    tx_data = TransactionCreate(
                        bank_account_id=account_uuid,
                        **formatted
                    )
                    await TransactionService.create_transaction(db, tx_data)
                    new_count += 1
                
                # Update sync timestamp
                bank_account.last_sync_at = datetime.utcnow()
                bank_account.sync_error = None
                await db.commit()
                
                logger.info(
                    f"Synced {new_count} new transactions for account {bank_account_id}"
                )
                
                return {"synced": new_count, "total": len(raw_transactions)}
                
            except BridgeAPIError as e:
                bank_account.sync_error = str(e)
                await db.commit()
                raise
            
            finally:
                await bridge_client.close()
    
    except Exception as e:
        logger.error(f"Failed to sync bank account {bank_account_id}: {e}")
        raise self.retry(exc=e, countdown=180 * (2 ** self.request.retries))


@celery_app.task(
    bind=True,
    base=AsyncTask,
    max_retries=2,
    time_limit=3600,  # 1 hour
)
async def sync_all_bank_accounts_task(self):
    """
    Sync all active bank accounts.
    """
    try:
        async with SessionLocal() as db:
            from sqlalchemy import select
            from app.models.bank_account import BankAccount
            
            # Get all active bank accounts with Bridge ID
            result = await db.execute(
                select(BankAccount).where(
                    BankAccount.is_active == True,
                    BankAccount.bridge_account_id.is_not(None),
                    BankAccount.deleted_at.is_(None)
                )
            )
            
            accounts = result.scalars().all()
            
            logger.info(f"Syncing {len(accounts)} bank accounts")
            
            # Queue sync tasks
            for account in accounts:
                sync_bank_account_task.delay(str(account.id))
            
            return {"queued": len(accounts)}
    
    except Exception as e:
        logger.error(f"Failed to queue bank account syncs: {e}")
        return {"error": str(e)}


@celery_app.task(
    bind=True,
    base=AsyncTask,
    max_retries=3,
    time_limit=300
)
async def auto_reconcile_transaction_task(self, transaction_id: str):
    """
    Auto-reconcile a transaction with fuzzy AI matching.
    
    Args:
        transaction_id: Transaction UUID
    """
    try:
        async with SessionLocal() as db:
            from uuid import UUID
            from app.models.transaction import Transaction
            from app.models.bank_account import BankAccount
            
            transaction_uuid = UUID(transaction_id)
            
            # Get transaction
            transaction = await db.get(Transaction, transaction_uuid)
            if not transaction:
                logger.error(f"Transaction {transaction_id} not found")
                return {"error": "Transaction not found"}
            
            # Get user_id
            bank_account = await db.get(BankAccount, transaction.bank_account_id)
            if not bank_account:
                return {"error": "Bank account not found"}
            
            # Attempt auto-reconciliation
            ai_client = ClaudeClient()
            reconciliation = await ReconciliationService.auto_reconcile_transaction(
                db,
                bank_account.user_id,
                transaction_uuid,
                ai_client
            )
            
            if reconciliation:
                await db.commit()
                logger.info(f"Auto-reconciled transaction {transaction_id}")
                return {"reconciled": True, "reconciliation_id": str(reconciliation.id)}
            else:
                logger.info(f"No auto-reconciliation match for transaction {transaction_id}")
                return {"reconciled": False}
    
    except Exception as e:
        logger.error(f"Failed to auto-reconcile transaction {transaction_id}: {e}")
        raise self.retry(exc=e, countdown=60 * (2 ** self.request.retries))


