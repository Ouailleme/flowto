"""Bank Account API endpoints"""
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Dict
from pydantic import BaseModel

from app.core.database import get_db
from app.api.deps import get_current_user
from app.models.user import User
from app.models.bank_account import BankAccount
from app.schemas.bank import BankAccountCreate, BankAccountUpdate, BankAccountRead, BankAccountList
from app.services.bank_service import BankService
from app.integrations.bridge_client import BridgeClient, BridgeAPIError

router = APIRouter(prefix="/banks", tags=["banks"])


class BridgeConnectRequest(BaseModel):
    """Request to initiate Bridge connection"""
    pass


class BridgeCallbackRequest(BaseModel):
    """Callback data from Bridge after successful connection"""
    user_uuid: str
    item_id: str


@router.post(
    "/",
    response_model=BankAccountRead,
    status_code=status.HTTP_201_CREATED,
    summary="Create bank account"
)
async def create_bank_account(
    account_data: BankAccountCreate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
) -> BankAccount:
    """
    Create a new bank account.
    
    Normally bank accounts are created via Bridge API connection,
    but this endpoint allows manual entry.
    """
    account = await BankService.create_bank_account(
        db,
        current_user.id,
        account_data
    )
    return account


@router.get(
    "/",
    response_model=BankAccountList,
    summary="List bank accounts"
)
async def list_bank_accounts(
    is_active: bool | None = None,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
) -> BankAccountList:
    """
    Get all bank accounts for current user.
    
    - **is_active**: Filter by active status (optional)
    """
    accounts = await BankService.get_user_bank_accounts(
        db,
        current_user.id,
        is_active
    )
    
    return BankAccountList(
        accounts=accounts,
        total=len(accounts)
    )


@router.get(
    "/{account_id}",
    response_model=BankAccountRead,
    summary="Get bank account"
)
async def get_bank_account(
    account_id: str,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
) -> BankAccount:
    """Get a specific bank account by ID"""
    from uuid import UUID
    
    try:
        account_uuid = UUID(account_id)
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid account ID format"
        )
    
    account = await BankService.get_bank_account(
        db,
        account_uuid,
        current_user.id
    )
    
    if not account:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Bank account not found"
        )
    
    return account


@router.patch(
    "/{account_id}",
    response_model=BankAccountRead,
    summary="Update bank account"
)
async def update_bank_account(
    account_id: str,
    update_data: BankAccountUpdate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
) -> BankAccount:
    """Update a bank account"""
    from uuid import UUID
    
    try:
        account_uuid = UUID(account_id)
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid account ID format"
        )
    
    account = await BankService.get_bank_account(
        db,
        account_uuid,
        current_user.id
    )
    
    if not account:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Bank account not found"
        )
    
    account = await BankService.update_bank_account(
        db,
        account,
        update_data
    )
    
    return account


@router.delete(
    "/{account_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete bank account"
)
async def delete_bank_account(
    account_id: str,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
) -> None:
    """Soft delete a bank account"""
    from uuid import UUID
    
    try:
        account_uuid = UUID(account_id)
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid account ID format"
        )
    
    account = await BankService.get_bank_account(
        db,
        account_uuid,
        current_user.id
    )
    
    if not account:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Bank account not found"
        )
    
    await BankService.delete_bank_account(db, account)


@router.post(
    "/connect/initiate",
    summary="Initiate Bridge bank connection"
)
async def initiate_bridge_connection(
    current_user: User = Depends(get_current_user),
) -> Dict:
    """
    Initiate connection to bank via Bridge API.
    
    Returns connect URL for user to authorize bank access in their browser.
    """
    try:
        bridge_client = BridgeClient()
        
        # Generate Bridge connect URL
        auth_data = await bridge_client.authenticate_user(
            email=current_user.email,
            password=""  # Bridge will handle authentication
        )
        
        await bridge_client.close()
        
        return {
            "connect_url": auth_data.get("redirect_url"),
            "message": "Redirectez l'utilisateur vers cette URL pour connecter sa banque"
        }
        
    except BridgeAPIError as e:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=f"Bridge API error: {str(e)}"
        )


@router.post(
    "/connect/callback",
    response_model=List[BankAccountRead],
    summary="Handle Bridge connection callback"
)
async def handle_bridge_callback(
    callback_data: BridgeCallbackRequest,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
) -> List[BankAccount]:
    """
    Handle callback after successful Bridge connection.
    
    Fetches accounts from Bridge and creates them in our database.
    """
    try:
        bridge_client = BridgeClient()
        
        # Fetch accounts from Bridge
        bridge_accounts = await bridge_client.get_accounts(
            user_uuid=callback_data.user_uuid
        )
        
        created_accounts = []
        
        # Create accounts in our database
        for bridge_account in bridge_accounts:
            account = await BankService.connect_bridge_account(
                db=db,
                user_id=current_user.id,
                bridge_account_data=bridge_account,
                bridge_user_uuid=callback_data.user_uuid
            )
            created_accounts.append(account)
        
        await db.commit()
        await bridge_client.close()
        
        logger.info(
            f"Created {len(created_accounts)} accounts from Bridge "
            f"for user {current_user.id}"
        )
        
        return created_accounts
        
    except BridgeAPIError as e:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=f"Bridge API error: {str(e)}"
        )
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.post(
    "/{account_id}/sync",
    summary="Sync transactions from Bridge"
)
async def sync_transactions(
    account_id: str,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
) -> Dict:
    """
    Sync transactions from Bridge API for a specific account.
    
    Returns statistics about synced transactions.
    """
    from uuid import UUID
    
    try:
        account_uuid = UUID(account_id)
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid account ID format"
        )
    
    # Get account
    account = await BankService.get_bank_account(
        db,
        account_uuid,
        current_user.id
    )
    
    if not account:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Bank account not found"
        )
    
    if not account.bridge_account_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Account is not connected to Bridge API"
        )
    
    # Sync transactions
    try:
        bridge_client = BridgeClient()
        
        sync_result = await BankService.sync_transactions(
            db=db,
            account=account,
            bridge_client=bridge_client
        )
        
        await db.commit()
        await bridge_client.close()
        
        return sync_result
        
    except BridgeAPIError as e:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=f"Bridge API error: {str(e)}"
        )
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


import logging
logger = logging.getLogger(__name__)
