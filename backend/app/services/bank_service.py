"""Bank Account service - Business logic"""
from typing import Optional, List, Dict
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_
from uuid import UUID
from datetime import datetime
import logging

from app.models.bank_account import BankAccount
from app.models.user import User
from app.models.transaction import Transaction
from app.schemas.bank import BankAccountCreate, BankAccountUpdate
from app.integrations.bridge_client import BridgeClient, BridgeAPIError

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
        account.deleted_at = datetime.utcnow()
        account.is_active = False
        await db.flush()
        
        logger.info(f"Bank account deleted: {account.id}")
    
    @staticmethod
    async def connect_bridge_account(
        db: AsyncSession,
        user_id: UUID,
        bridge_account_data: Dict,
        bridge_user_uuid: str
    ) -> BankAccount:
        """
        Create bank account from Bridge API connection.
        
        Args:
            db: Database session
            user_id: User ID
            bridge_account_data: Raw account data from Bridge API
            bridge_user_uuid: Bridge user UUID
            
        Returns:
            Created bank account
        """
        # Check if account already exists (by bridge_account_id)
        bridge_account_id = str(bridge_account_data.get("id"))
        result = await db.execute(
            select(BankAccount).where(
                and_(
                    BankAccount.user_id == user_id,
                    BankAccount.bridge_account_id == bridge_account_id,
                    BankAccount.deleted_at.is_(None)
                )
            )
        )
        existing_account = result.scalar_one_or_none()
        
        if existing_account:
            logger.info(f"Bridge account {bridge_account_id} already exists, updating...")
            existing_account.balance = float(bridge_account_data.get("balance", 0))
            existing_account.is_active = True
            existing_account.last_sync_at = datetime.utcnow()
            await db.flush()
            return existing_account
        
        # Create new account
        account = BankAccount(
            user_id=user_id,
            bank_name=bridge_account_data.get("bank_name", "Unknown Bank"),
            account_type=bridge_account_data.get("type", "checking"),
            iban=bridge_account_data.get("iban"),
            balance=float(bridge_account_data.get("balance", 0)),
            currency=bridge_account_data.get("currency_code", "EUR"),
            bridge_account_id=bridge_account_id,
            bridge_user_uuid=bridge_user_uuid,
            bridge_item_id=str(bridge_account_data.get("item_id")),
            is_active=True,
            last_sync_at=datetime.utcnow(),
        )
        
        db.add(account)
        await db.flush()
        
        logger.info(f"Bridge account created: {account.id} (Bridge ID: {bridge_account_id})")
        return account
    
    @staticmethod
    async def sync_transactions(
        db: AsyncSession,
        account: BankAccount,
        bridge_client: BridgeClient
    ) -> Dict:
        """
        Sync transactions from Bridge API for a bank account.
        
        Args:
            db: Database session
            account: Bank account to sync
            bridge_client: Bridge API client
            
        Returns:
            Dict with sync stats (new_count, updated_count)
        """
        if not account.bridge_account_id:
            raise ValueError("Account is not connected to Bridge API")
        
        # Get transactions since last sync (or last 90 days)
        last_sync = account.last_sync_at or (datetime.utcnow() - timedelta(days=90))
        
        try:
            # Fetch transactions from Bridge
            raw_transactions = await bridge_client.sync_account_transactions(
                account_id=int(account.bridge_account_id),
                last_sync=last_sync
            )
            
            new_count = 0
            updated_count = 0
            
            for raw_tx in raw_transactions:
                # Format transaction
                formatted_tx = bridge_client.format_transaction(raw_tx)
                bridge_tx_id = formatted_tx["bridge_transaction_id"]
                
                # Check if transaction already exists
                result = await db.execute(
                    select(Transaction).where(
                        and_(
                            Transaction.bank_account_id == account.id,
                            Transaction.bridge_transaction_id == bridge_tx_id
                        )
                    )
                )
                existing_tx = result.scalar_one_or_none()
                
                if existing_tx:
                    # Update existing transaction (in case of correction)
                    existing_tx.description = formatted_tx["description"]
                    existing_tx.amount = formatted_tx["amount"]
                    updated_count += 1
                else:
                    # Create new transaction
                    transaction = Transaction(
                        user_id=account.user_id,
                        bank_account_id=account.id,
                        bridge_transaction_id=bridge_tx_id,
                        description=formatted_tx["description"],
                        amount=formatted_tx["amount"],
                        currency=formatted_tx["currency"],
                        date=formatted_tx["date"],
                        transaction_type=formatted_tx["transaction_type"],
                        raw_data=formatted_tx["raw_data"],
                    )
                    db.add(transaction)
                    new_count += 1
            
            # Update last sync timestamp
            account.last_sync_at = datetime.utcnow()
            
            # Update account balance
            balance_info = await bridge_client.get_account_balance(
                int(account.bridge_account_id)
            )
            account.balance = float(balance_info.get("balance", account.balance))
            
            await db.flush()
            
            logger.info(
                f"Synced {new_count} new and {updated_count} updated transactions "
                f"for account {account.id}"
            )
            
            return {
                "new_count": new_count,
                "updated_count": updated_count,
                "last_sync": account.last_sync_at.isoformat(),
                "balance": account.balance,
            }
            
        except BridgeAPIError as e:
            logger.error(f"Bridge sync failed for account {account.id}: {e}")
            raise ValueError(f"Failed to sync transactions: {e}")

from datetime import timedelta

