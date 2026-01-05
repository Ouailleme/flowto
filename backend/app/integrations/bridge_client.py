"""Bridge API client for bank data synchronization"""
import httpx
from typing import List, Dict, Optional
from datetime import datetime, timedelta
from tenacity import retry, stop_after_attempt, wait_exponential
import logging

from app.config import settings

logger = logging.getLogger(__name__)


class BridgeAPIError(Exception):
    """Bridge API error"""
    pass


class BridgeClient:
    """
    Client for Bridge API (banking aggregation)
    
    Doc: https://docs.bridgeapi.io/
    """
    
    BASE_URL = "https://api.bridgeapi.io/v2"
    
    def __init__(self, api_key: str = None, client_id: str = None, client_secret: str = None):
        """Initialize Bridge client"""
        self.api_key = api_key or settings.BRIDGE_API_KEY
        self.client_id = client_id or settings.BRIDGE_CLIENT_ID
        self.client_secret = client_secret or settings.BRIDGE_CLIENT_SECRET
        
        self.client = httpx.AsyncClient(
            timeout=30.0,
            headers={
                "Bridge-Version": "2021-06-01",
                "Client-Id": self.client_id,
                "Client-Secret": self.client_secret,
            }
        )
    
    async def close(self):
        """Close HTTP client"""
        await self.client.aclose()
    
    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=2, max=10)
    )
    async def authenticate_user(self, email: str, password: str) -> Dict:
        """
        Authenticate user with their bank credentials.
        
        Returns connect URL for user to authorize bank access.
        """
        try:
            response = await self.client.post(
                f"{self.BASE_URL}/connect/items/add",
                json={
                    "prefill_email": email,
                }
            )
            response.raise_for_status()
            
            data = response.json()
            logger.info(f"Bridge authentication initiated for {email}")
            return data
            
        except httpx.HTTPStatusError as e:
            logger.error(f"Bridge authentication failed: {e.response.text}")
            raise BridgeAPIError(f"Bridge authentication failed: {e}")
        except httpx.RequestError as e:
            logger.error(f"Bridge request error: {e}")
            raise BridgeAPIError(f"Bridge request error: {e}")
    
    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=2, max=10)
    )
    async def get_accounts(self, user_uuid: str) -> List[Dict]:
        """
        Get all bank accounts for a user.
        
        Args:
            user_uuid: Bridge user UUID
            
        Returns:
            List of bank accounts
        """
        try:
            response = await self.client.get(
                f"{self.BASE_URL}/accounts",
                params={"user_uuid": user_uuid}
            )
            response.raise_for_status()
            
            data = response.json()
            accounts = data.get("resources", [])
            
            logger.info(f"Fetched {len(accounts)} accounts for user {user_uuid}")
            return accounts
            
        except httpx.HTTPStatusError as e:
            logger.error(f"Bridge get accounts failed: {e.response.text}")
            raise BridgeAPIError(f"Failed to get accounts: {e}")
        except httpx.RequestError as e:
            logger.error(f"Bridge request error: {e}")
            raise BridgeAPIError(f"Bridge request error: {e}")
    
    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=2, max=10)
    )
    async def get_transactions(
        self,
        account_id: int,
        since: Optional[datetime] = None,
        until: Optional[datetime] = None,
        limit: int = 500
    ) -> List[Dict]:
        """
        Get transactions for a bank account.
        
        Args:
            account_id: Bridge account ID
            since: Start date (default: 90 days ago)
            until: End date (default: today)
            limit: Max number of transactions (default: 500)
            
        Returns:
            List of transactions
        """
        if since is None:
            since = datetime.utcnow() - timedelta(days=90)
        
        if until is None:
            until = datetime.utcnow()
        
        try:
            response = await self.client.get(
                f"{self.BASE_URL}/accounts/{account_id}/transactions",
                params={
                    "since": since.strftime("%Y-%m-%d"),
                    "until": until.strftime("%Y-%m-%d"),
                    "limit": limit
                }
            )
            response.raise_for_status()
            
            data = response.json()
            transactions = data.get("resources", [])
            
            logger.info(
                f"Fetched {len(transactions)} transactions for account {account_id} "
                f"from {since.date()} to {until.date()}"
            )
            return transactions
            
        except httpx.HTTPStatusError as e:
            logger.error(f"Bridge get transactions failed: {e.response.text}")
            raise BridgeAPIError(f"Failed to get transactions: {e}")
        except httpx.RequestError as e:
            logger.error(f"Bridge request error: {e}")
            raise BridgeAPIError(f"Bridge request error: {e}")
    
    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=2, max=10)
    )
    async def get_account_balance(self, account_id: int) -> Dict:
        """
        Get current balance for a bank account.
        
        Args:
            account_id: Bridge account ID
            
        Returns:
            Account balance info
        """
        try:
            response = await self.client.get(
                f"{self.BASE_URL}/accounts/{account_id}"
            )
            response.raise_for_status()
            
            data = response.json()
            
            logger.info(f"Fetched balance for account {account_id}")
            return {
                "balance": data.get("balance"),
                "currency": data.get("currency_code"),
                "updated_at": data.get("updated_at")
            }
            
        except httpx.HTTPStatusError as e:
            logger.error(f"Bridge get balance failed: {e.response.text}")
            raise BridgeAPIError(f"Failed to get balance: {e}")
        except httpx.RequestError as e:
            logger.error(f"Bridge request error: {e}")
            raise BridgeAPIError(f"Bridge request error: {e}")
    
    async def sync_account_transactions(
        self,
        account_id: int,
        last_sync: Optional[datetime] = None
    ) -> List[Dict]:
        """
        Sync transactions since last sync.
        
        Args:
            account_id: Bridge account ID
            last_sync: Last sync datetime (default: 30 days ago)
            
        Returns:
            List of new transactions
        """
        if last_sync is None:
            last_sync = datetime.utcnow() - timedelta(days=30)
        
        transactions = await self.get_transactions(
            account_id=account_id,
            since=last_sync
        )
        
        return transactions
    
    def format_transaction(self, raw_transaction: Dict) -> Dict:
        """
        Format Bridge transaction to our internal format.
        
        Args:
            raw_transaction: Raw transaction from Bridge API
            
        Returns:
            Formatted transaction
        """
        return {
            "bridge_transaction_id": str(raw_transaction.get("id")),
            "description": raw_transaction.get("clean_description") or raw_transaction.get("raw_description"),
            "amount": float(raw_transaction.get("amount", 0)),
            "currency": raw_transaction.get("currency_code", "EUR"),
            "date": datetime.fromisoformat(raw_transaction.get("date").replace("Z", "+00:00")),
            "transaction_type": "credit" if raw_transaction.get("amount", 0) > 0 else "debit",
            "raw_data": raw_transaction,
        }


