"""Invoice API endpoints"""
from fastapi import APIRouter, Depends, HTTPException, status, Query
from fastapi.responses import Response
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional
from datetime import date
from pydantic import BaseModel, EmailStr

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
from app.services.pdf_service import PDFService
from app.integrations.sendgrid_client import SendGridClient

router = APIRouter(prefix="/invoices", tags=["invoices"])


class SendInvoiceRequest(BaseModel):
    """Request to send invoice by email"""
    recipient_email: EmailStr
    subject: str | None = None
    message: str | None = None


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


@router.get(
    "/{invoice_id}/pdf",
    summary="Download invoice PDF"
)
async def download_invoice_pdf(
    invoice_id: str,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
) -> Response:
    """
    Download invoice as PDF.
    
    Returns PDF file for download.
    """
    from uuid import UUID
    
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
    
    # Generate PDF
    try:
        pdf_bytes = PDFService.generate_invoice_pdf(invoice, current_user)
        filename = PDFService.get_invoice_filename(invoice)
        
        return Response(
            content=pdf_bytes,
            media_type="application/pdf",
            headers={
                "Content-Disposition": f'attachment; filename="{filename}"'
            }
        )
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )


@router.post(
    "/{invoice_id}/send",
    summary="Send invoice by email"
)
async def send_invoice_email(
    invoice_id: str,
    send_request: SendInvoiceRequest,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Send invoice by email with PDF attachment.
    
    - **recipient_email**: Email address to send to
    - **subject**: Email subject (optional, default generated)
    - **message**: Email message (optional, default generated)
    """
    from uuid import UUID
    
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
    
    # Generate PDF
    try:
        pdf_bytes = PDFService.generate_invoice_pdf(invoice, current_user)
        filename = PDFService.get_invoice_filename(invoice)
        
        # Prepare email
        subject = send_request.subject or f"Facture {invoice.invoice_number} - {current_user.company_name}"
        
        message = send_request.message or f"""
Bonjour,

Veuillez trouver ci-joint la facture {invoice.invoice_number} d'un montant de {invoice.total_amount:.2f} {invoice.currency}.

Date d'échéance : {invoice.due_date.strftime('%d/%m/%Y')}

Cordialement,
{current_user.company_name}
        """.strip()
        
        # Send email
        email_client = SendGridClient()
        await email_client.send_email_with_attachment(
            to_email=send_request.recipient_email,
            subject=subject,
            content=message,
            attachment_content=pdf_bytes,
            attachment_filename=filename,
            attachment_type="application/pdf"
        )
        
        return {
            "message": "Invoice sent successfully",
            "recipient": send_request.recipient_email,
            "invoice_number": invoice.invoice_number
        }
        
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to generate PDF: {str(e)}"
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to send email: {str(e)}"
        )


