"""Transaction categorization API endpoints"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.api.deps import get_current_user
from app.models.user import User
from app.schemas.transaction import TransactionRead
from app.services.categorization_service import CategorizationService
from app.services.transaction_service import TransactionService
from app.integrations.claude_client import ClaudeClient

router = APIRouter(prefix="/categorization", tags=["categorization"])


@router.post(
    "/transactions/{transaction_id}",
    response_model=TransactionRead,
    summary="Categorize transaction"
)
async def categorize_transaction(
    transaction_id: str,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Categorize a single transaction using AI.
    
    Returns the transaction with updated category and confidence.
    """
    from uuid import UUID
    
    try:
        transaction_uuid = UUID(transaction_id)
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid transaction ID format"
        )
    
    # Get transaction
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
    
    # Categorize
    ai_client = ClaudeClient()
    transaction = await CategorizationService.categorize_transaction(
        db,
        transaction,
        ai_client
    )
    
    await db.commit()
    return transaction


@router.post(
    "/bulk",
    summary="Categorize all uncategorized transactions"
)
async def categorize_uncategorized(
    limit: int = 50,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Categorize all uncategorized transactions for current user.
    
    - **limit**: Max number of transactions to categorize (default 50)
    
    Returns count of transactions categorized.
    """
    ai_client = ClaudeClient()
    count = await CategorizationService.categorize_uncategorized_transactions(
        db,
        current_user.id,
        limit,
        ai_client
    )
    
    return {"categorized": count}


@router.get(
    "/breakdown",
    summary="Get category breakdown"
)
async def get_category_breakdown(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Get spending breakdown by category for current user.
    
    Returns dict of category → total amount.
    """
    breakdown = await CategorizationService.get_category_breakdown(
        db,
        current_user.id
    )
    return breakdown


