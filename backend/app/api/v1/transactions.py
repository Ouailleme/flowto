"""Transaction API endpoints"""
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional
from datetime import datetime

from app.core.database import get_db
from app.api.deps import get_current_user
from app.models.user import User
from app.models.transaction import Transaction
from app.schemas.transaction import (
    TransactionRead,
    TransactionUpdate,
    TransactionFilter,
    TransactionList
)
from app.services.transaction_service import TransactionService

router = APIRouter(prefix="/transactions", tags=["transactions"])


@router.get(
    "/",
    response_model=TransactionList,
    summary="List transactions"
)
async def list_transactions(
    bank_account_id: Optional[str] = None,
    start_date: Optional[datetime] = None,
    end_date: Optional[datetime] = None,
    category: Optional[str] = None,
    is_reconciled: Optional[bool] = None,
    min_amount: Optional[float] = None,
    max_amount: Optional[float] = None,
    search: Optional[str] = None,
    page: int = Query(1, ge=1),
    page_size: int = Query(50, ge=1, le=100),
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
) -> TransactionList:
    """
    Get transactions with filters and pagination.
    
    - **bank_account_id**: Filter by bank account
    - **start_date**: Filter by date range (start)
    - **end_date**: Filter by date range (end)
    - **category**: Filter by category
    - **is_reconciled**: Filter by reconciliation status
    - **min_amount / max_amount**: Filter by amount range
    - **search**: Search in description
    - **page**: Page number (default 1)
    - **page_size**: Items per page (default 50, max 100)
    """
    from uuid import UUID
    from decimal import Decimal
    
    # Build filters
    filters = TransactionFilter(
        bank_account_id=UUID(bank_account_id) if bank_account_id else None,
        start_date=start_date,
        end_date=end_date,
        category=category,
        is_reconciled=is_reconciled,
        min_amount=Decimal(str(min_amount)) if min_amount is not None else None,
        max_amount=Decimal(str(max_amount)) if max_amount is not None else None,
        search=search
    )
    
    transactions, total = await TransactionService.get_transactions(
        db,
        current_user.id,
        filters,
        page,
        page_size
    )
    
    total_pages = (total + page_size - 1) // page_size
    
    return TransactionList(
        transactions=transactions,
        total=total,
        page=page,
        page_size=page_size,
        total_pages=total_pages
    )


@router.get(
    "/{transaction_id}",
    response_model=TransactionRead,
    summary="Get transaction"
)
async def get_transaction(
    transaction_id: str,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
) -> Transaction:
    """Get a specific transaction by ID"""
    from uuid import UUID
    
    try:
        transaction_uuid = UUID(transaction_id)
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid transaction ID format"
        )
    
    transaction = await TransactionService.get_transaction(
        db,
        transaction_uuid,
        current_user.id
    )
    
    if not transaction:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Transaction not found"
        )
    
    return transaction


@router.patch(
    "/{transaction_id}",
    response_model=TransactionRead,
    summary="Update transaction"
)
async def update_transaction(
    transaction_id: str,
    update_data: TransactionUpdate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
) -> Transaction:
    """
    Update a transaction.
    
    Mainly used for manual category correction.
    """
    from uuid import UUID
    
    try:
        transaction_uuid = UUID(transaction_id)
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid transaction ID format"
        )
    
    transaction = await TransactionService.get_transaction(
        db,
        transaction_uuid,
        current_user.id
    )
    
    if not transaction:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Transaction not found"
        )
    
    transaction = await TransactionService.update_transaction(
        db,
        transaction,
        update_data
    )
    
    return transaction


