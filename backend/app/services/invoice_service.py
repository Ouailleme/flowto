"""Invoice service - Business logic"""
from typing import Optional, List, Tuple
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_, func
from uuid import UUID
from datetime import date, datetime
import logging

from app.models.invoice import Invoice
from app.schemas.invoice import InvoiceCreate, InvoiceUpdate, InvoiceFilter

logger = logging.getLogger(__name__)


class InvoiceService:
    """Invoice service"""
    
    @staticmethod
    async def create_invoice(
        db: AsyncSession,
        user_id: UUID,
        invoice_data: InvoiceCreate
    ) -> Invoice:
        """
        Create a new invoice.
        
        Calculates total_amount and validates business rules.
        """
        # Check for duplicate invoice number for this user
        result = await db.execute(
            select(Invoice).where(
                and_(
                    Invoice.user_id == user_id,
                    Invoice.invoice_number == invoice_data.invoice_number,
                    Invoice.deleted_at.is_(None)
                )
            )
        )
        if result.scalar_one_or_none():
            raise ValueError(f"Invoice number {invoice_data.invoice_number} already exists")
        
        # Calculate total
        total_amount = invoice_data.amount + invoice_data.tax_amount
        
        # Determine initial status
        today = date.today()
        if invoice_data.due_date < today:
            status = "overdue"
        else:
            status = "pending"
        
        invoice = Invoice(
            user_id=user_id,
            invoice_number=invoice_data.invoice_number,
            client_name=invoice_data.client_name,
            client_email=invoice_data.client_email,
            client_address=invoice_data.client_address,
            amount=invoice_data.amount,
            tax_amount=invoice_data.tax_amount,
            total_amount=total_amount,
            currency=invoice_data.currency,
            issue_date=invoice_data.issue_date,
            due_date=invoice_data.due_date,
            status=status,
            description=invoice_data.description,
            notes=invoice_data.notes,
            is_reconciled=False,
        )
        
        db.add(invoice)
        await db.flush()
        
        logger.info(f"Invoice created: {invoice.id} ({invoice.invoice_number}) for user {user_id}")
        return invoice
    
    @staticmethod
    async def get_invoice(
        db: AsyncSession,
        invoice_id: UUID,
        user_id: UUID
    ) -> Optional[Invoice]:
        """Get invoice by ID with ownership check"""
        result = await db.execute(
            select(Invoice).where(
                and_(
                    Invoice.id == invoice_id,
                    Invoice.user_id == user_id,
                    Invoice.deleted_at.is_(None)
                )
            )
        )
        return result.scalar_one_or_none()
    
    @staticmethod
    async def get_invoices(
        db: AsyncSession,
        user_id: UUID,
        filters: InvoiceFilter,
        page: int = 1,
        page_size: int = 50
    ) -> Tuple[List[Invoice], int]:
        """
        Get invoices with filters and pagination.
        
        Returns:
            Tuple of (invoices list, total count)
        """
        # Base query
        query = select(Invoice).where(
            and_(
                Invoice.user_id == user_id,
                Invoice.deleted_at.is_(None)
            )
        )
        
        # Apply filters
        conditions = []
        
        if filters.status:
            conditions.append(Invoice.status == filters.status)
        
        if filters.is_reconciled is not None:
            conditions.append(Invoice.is_reconciled == filters.is_reconciled)
        
        if filters.start_date:
            conditions.append(Invoice.due_date >= filters.start_date)
        
        if filters.end_date:
            conditions.append(Invoice.due_date <= filters.end_date)
        
        if filters.client_name:
            conditions.append(
                Invoice.client_name.ilike(f"%{filters.client_name}%")
            )
        
        if filters.min_amount is not None:
            conditions.append(Invoice.total_amount >= filters.min_amount)
        
        if filters.max_amount is not None:
            conditions.append(Invoice.total_amount <= filters.max_amount)
        
        if conditions:
            query = query.where(and_(*conditions))
        
        # Count total
        count_query = select(func.count()).select_from(query.subquery())
        total_result = await db.execute(count_query)
        total = total_result.scalar() or 0
        
        # Apply pagination
        query = query.order_by(Invoice.due_date.desc())
        query = query.offset((page - 1) * page_size).limit(page_size)
        
        result = await db.execute(query)
        invoices = list(result.scalars().all())
        
        return invoices, total
    
    @staticmethod
    async def update_invoice(
        db: AsyncSession,
        invoice: Invoice,
        update_data: InvoiceUpdate
    ) -> Invoice:
        """Update invoice"""
        update_dict = update_data.model_dump(exclude_unset=True)
        
        # Recalculate total if amount or tax changed
        if "amount" in update_dict or "tax_amount" in update_dict:
            amount = update_dict.get("amount", invoice.amount)
            tax_amount = update_dict.get("tax_amount", invoice.tax_amount)
            update_dict["total_amount"] = amount + tax_amount
        
        for field, value in update_dict.items():
            setattr(invoice, field, value)
        
        await db.flush()
        
        logger.info(f"Invoice updated: {invoice.id}")
        return invoice
    
    @staticmethod
    async def mark_invoice_paid(
        db: AsyncSession,
        invoice: Invoice,
        payment_date: date
    ) -> Invoice:
        """Mark invoice as paid"""
        invoice.status = "paid"
        invoice.payment_date = payment_date
        await db.flush()
        
        logger.info(f"Invoice marked as paid: {invoice.id}")
        return invoice
    
    @staticmethod
    async def delete_invoice(
        db: AsyncSession,
        invoice: Invoice
    ) -> None:
        """Soft delete invoice"""
        invoice.deleted_at = datetime.utcnow()
        await db.flush()
        
        logger.info(f"Invoice deleted: {invoice.id}")
    
    @staticmethod
    async def get_overdue_invoices(
        db: AsyncSession,
        user_id: Optional[UUID] = None,
        days_overdue: int = 0
    ) -> List[Invoice]:
        """Get overdue invoices (for reminders)"""
        conditions = [
            Invoice.status.in_(["pending", "overdue"]),  # Include both pending and overdue
            Invoice.due_date < date.today(),
            Invoice.deleted_at.is_(None)
        ]
        
        if user_id:
            conditions.append(Invoice.user_id == user_id)
        
        result = await db.execute(
            select(Invoice)
            .where(and_(*conditions))
            .order_by(Invoice.due_date.asc())
        )
        return list(result.scalars().all())


