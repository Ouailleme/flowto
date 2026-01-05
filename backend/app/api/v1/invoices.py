"""Invoice API endpoints"""
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional
from datetime import date

from app.core.database import get_db
from app.api.deps import get_current_user
from app.models.user import User
from app.models.invoice import Invoice
from app.schemas.invoice import (
    InvoiceCreate,
    InvoiceUpdate,
    InvoiceRead,
    InvoiceFilter,
    InvoiceList
)
from app.services.invoice_service import InvoiceService

router = APIRouter(prefix="/invoices", tags=["invoices"])


@router.post(
    "/",
    response_model=InvoiceRead,
    status_code=status.HTTP_201_CREATED,
    summary="Create invoice"
)
async def create_invoice(
    invoice_data: InvoiceCreate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
) -> Invoice:
    """
    Create a new invoice.
    
    Invoice number must be unique for the user.
    """
    try:
        invoice = await InvoiceService.create_invoice(
            db,
            current_user.id,
            invoice_data
        )
        return invoice
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.get(
    "/",
    response_model=InvoiceList,
    summary="List invoices"
)
async def list_invoices(
    status: Optional[str] = None,
    is_reconciled: Optional[bool] = None,
    start_date: Optional[date] = None,
    end_date: Optional[date] = None,
    client_name: Optional[str] = None,
    min_amount: Optional[float] = None,
    max_amount: Optional[float] = None,
    page: int = Query(1, ge=1),
    page_size: int = Query(50, ge=1, le=100),
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
) -> InvoiceList:
    """
    Get invoices with filters and pagination.
    
    - **status**: pending, paid, overdue, cancelled
    - **is_reconciled**: Filter by reconciliation status
    - **start_date / end_date**: Filter by due date range
    - **client_name**: Search by client name
    - **min_amount / max_amount**: Filter by amount range
    """
    from decimal import Decimal
    
    filters = InvoiceFilter(
        status=status,
        is_reconciled=is_reconciled,
        start_date=start_date,
        end_date=end_date,
        client_name=client_name,
        min_amount=Decimal(str(min_amount)) if min_amount is not None else None,
        max_amount=Decimal(str(max_amount)) if max_amount is not None else None
    )
    
    invoices, total = await InvoiceService.get_invoices(
        db,
        current_user.id,
        filters,
        page,
        page_size
    )
    
    total_pages = (total + page_size - 1) // page_size
    
    return InvoiceList(
        invoices=invoices,
        total=total,
        page=page,
        page_size=page_size,
        total_pages=total_pages
    )


@router.get(
    "/{invoice_id}",
    response_model=InvoiceRead,
    summary="Get invoice"
)
async def get_invoice(
    invoice_id: str,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
) -> Invoice:
    """Get a specific invoice by ID"""
    from uuid import UUID
    
    try:
        invoice_uuid = UUID(invoice_id)
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid invoice ID format"
        )
    
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
    
    return invoice


@router.patch(
    "/{invoice_id}",
    response_model=InvoiceRead,
    summary="Update invoice"
)
async def update_invoice(
    invoice_id: str,
    update_data: InvoiceUpdate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
) -> Invoice:
    """Update an invoice"""
    from uuid import UUID
    
    try:
        invoice_uuid = UUID(invoice_id)
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid invoice ID format"
        )
    
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
    
    invoice = await InvoiceService.update_invoice(
        db,
        invoice,
        update_data
    )
    
    return invoice


@router.delete(
    "/{invoice_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete invoice"
)
async def delete_invoice(
    invoice_id: str,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
) -> None:
    """Soft delete an invoice"""
    from uuid import UUID
    
    try:
        invoice_uuid = UUID(invoice_id)
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid invoice ID format"
        )
    
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
    
    await InvoiceService.delete_invoice(db, invoice)


