"""Reconciliation API endpoints"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from app.core.database import get_db
from app.api.deps import get_current_user
from app.models.user import User
from app.schemas.reconciliation import (
    ReconciliationCreate,
    ReconciliationRead,
    ReconciliationSuggestion
)
from app.services.reconciliation_service import ReconciliationService
from app.integrations.claude_client import ClaudeClient

router = APIRouter(prefix="/reconciliations", tags=["reconciliations"])


@router.post(
    "/",
    response_model=ReconciliationRead,
    status_code=status.HTTP_201_CREATED,
    summary="Create reconciliation"
)
async def create_reconciliation(
    reconciliation_data: ReconciliationCreate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Create a reconciliation (link transaction to invoice).
    
    Can be manual (validated_by='user') or AI-suggested (validated_by='ai').
    """
    try:
        reconciliation = await ReconciliationService.create_reconciliation(
            db,
            current_user.id,
            reconciliation_data
        )
        await db.commit()
        return reconciliation
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.get(
    "/suggestions/{transaction_id}",
    response_model=List[ReconciliationSuggestion],
    summary="Get reconciliation suggestions"
)
async def get_reconciliation_suggestions(
    transaction_id: str,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Get AI-powered reconciliation suggestions for a transaction.
    
    Returns up to 5 best matching invoices with confidence scores.
    """
    from uuid import UUID
    
    try:
        transaction_uuid = UUID(transaction_id)
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid transaction ID format"
        )
    
    try:
        ai_client = ClaudeClient()
        suggestions = await ReconciliationService.suggest_reconciliations(
            db,
            current_user.id,
            transaction_uuid,
            ai_client
        )
        return suggestions
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )


@router.post(
    "/auto-reconcile/{transaction_id}",
    response_model=ReconciliationRead,
    summary="Auto-reconcile transaction"
)
async def auto_reconcile_transaction(
    transaction_id: str,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Automatically reconcile a transaction if high-confidence match found.
    
    Returns reconciliation if auto-matched, 404 if no match found.
    """
    from uuid import UUID
    
    try:
        transaction_uuid = UUID(transaction_id)
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid transaction ID format"
        )
    
    try:
        ai_client = ClaudeClient()
        reconciliation = await ReconciliationService.auto_reconcile_transaction(
            db,
            current_user.id,
            transaction_uuid,
            ai_client
        )
        
        if not reconciliation:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="No high-confidence match found for auto-reconciliation"
            )
        
        await db.commit()
        return reconciliation
        
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )


@router.get(
    "/stats",
    summary="Get reconciliation stats"
)
async def get_reconciliation_stats(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Get reconciliation statistics for current user.
    
    Returns counts by method, validator, and auto-reconciliation rate.
    """
    stats = await ReconciliationService.get_reconciliation_stats(
        db,
        current_user.id
    )
    return stats


