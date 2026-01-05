"""Bank Account API endpoints"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from app.core.database import get_db
from app.api.deps import get_current_user
from app.models.user import User
from app.models.bank_account import BankAccount
from app.schemas.bank import BankAccountCreate, BankAccountUpdate, BankAccountRead, BankAccountList
from app.services.bank_service import BankService

router = APIRouter(prefix="/banks", tags=["banks"])


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


