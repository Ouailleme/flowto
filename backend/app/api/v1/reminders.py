"""Reminder API endpoints"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.api.deps import get_current_user
from app.models.user import User
from app.schemas.reminder import ReminderRead
from app.services.reminder_service import ReminderService
from app.services.invoice_service import InvoiceService
from app.integrations.claude_client import ClaudeClient
from app.integrations.sendgrid_client import SendGridClient

router = APIRouter(prefix="/reminders", tags=["reminders"])


@router.post(
    "/invoices/{invoice_id}/send",
    response_model=ReminderRead,
    summary="Send payment reminder"
)
async def send_reminder(
    invoice_id: str,
    reminder_type: str,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Send a payment reminder for an invoice.
    
    - **invoice_id**: Invoice UUID
    - **reminder_type**: first, second, final
    """
    from uuid import UUID
    
    if reminder_type not in ["first", "second", "final"]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="reminder_type must be 'first', 'second', or 'final'"
        )
    
    try:
        invoice_uuid = UUID(invoice_id)
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid invoice ID format"
        )
    
    # Get invoice
    invoice = await InvoiceService.get_invoice(
        db,
        invoice_uuid,
        current_user.id
    )
    
    if not invoice:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Invoice not found"
        )
    
    # Send reminder
    try:
        ai_client = ClaudeClient()
        email_client = SendGridClient()
        
        reminder = await ReminderService.send_reminder(
            db,
            invoice,
            reminder_type,
            ai_client,
            email_client
        )
        
        await db.commit()
        return reminder
        
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.post(
    "/process-overdue",
    summary="Process all overdue invoices"
)
async def process_overdue_invoices(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Process all overdue invoices and send appropriate reminders.
    
    Returns stats with counts of reminders sent.
    """
    ai_client = ClaudeClient()
    email_client = SendGridClient()
    
    stats = await ReminderService.process_overdue_invoices(
        db,
        current_user.id,
        ai_client,
        email_client
    )
    
    return stats


@router.get(
    "/stats",
    summary="Get reminder stats"
)
async def get_reminder_stats(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Get reminder statistics for current user.
    
    Returns total reminders, breakdown by type, and open rate.
    """
    stats = await ReminderService.get_reminder_stats(
        db,
        current_user.id
    )
    return stats


