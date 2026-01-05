"""Unit tests for InvoiceService"""
import pytest
from datetime import date, timedelta
from decimal import Decimal

from app.services.invoice_service import InvoiceService
from app.schemas.invoice import InvoiceCreate, InvoiceUpdate, InvoiceFilter


@pytest.mark.asyncio
class TestInvoiceService:
    """Test InvoiceService"""
    
    async def test_create_invoice(
        self,
        db_session,
        test_user,
        invoice_factory
    ):
        """Test creating an invoice"""
        data = InvoiceCreate(**invoice_factory())
        
        invoice = await InvoiceService.create_invoice(
            db_session,
            test_user.id,
            data
        )
        
        assert invoice.id is not None
        assert invoice.user_id == test_user.id
        assert invoice.invoice_number == data.invoice_number
        assert invoice.client_name == data.client_name
        assert invoice.amount == data.amount
        assert invoice.total_amount == data.amount + data.tax_amount
        assert invoice.status == "pending"
        assert invoice.is_reconciled is False
    
    async def test_create_invoice_duplicate_number(
        self,
        db_session,
        test_user,
        invoice_factory
    ):
        """Test that duplicate invoice numbers are rejected"""
        invoice_number = "INV-DUP-001"
        data = InvoiceCreate(**invoice_factory(invoice_number=invoice_number))
        
        # Create first invoice
        await InvoiceService.create_invoice(
            db_session,
            test_user.id,
            data
        )
        await db_session.commit()
        
        # Try to create duplicate
        with pytest.raises(ValueError, match="already exists"):
            await InvoiceService.create_invoice(
                db_session,
                test_user.id,
                data
            )
    
    async def test_create_invoice_overdue_status(
        self,
        db_session,
        test_user,
        invoice_factory
    ):
        """Test that invoice with past due date gets 'overdue' status"""
        data = InvoiceCreate(**invoice_factory(
            due_date=date.today() - timedelta(days=5)
        ))
        
        invoice = await InvoiceService.create_invoice(
            db_session,
            test_user.id,
            data
        )
        
        assert invoice.status == "overdue"
    
    async def test_get_invoice(
        self,
        db_session,
        test_user,
        invoice_factory
    ):
        """Test getting an invoice by ID"""
        data = InvoiceCreate(**invoice_factory())
        invoice = await InvoiceService.create_invoice(
            db_session,
            test_user.id,
            data
        )
        await db_session.commit()
        
        retrieved = await InvoiceService.get_invoice(
            db_session,
            invoice.id,
            test_user.id
        )
        
        assert retrieved is not None
        assert retrieved.id == invoice.id
        assert retrieved.invoice_number == invoice.invoice_number
    
    async def test_get_invoice_wrong_user(
        self,
        db_session,
        test_user,
        test_user_2,
        invoice_factory
    ):
        """Test that user cannot access another user's invoice"""
        data = InvoiceCreate(**invoice_factory())
        invoice = await InvoiceService.create_invoice(
            db_session,
            test_user.id,
            data
        )
        await db_session.commit()
        
        retrieved = await InvoiceService.get_invoice(
            db_session,
            invoice.id,
            test_user_2.id
        )
        
        assert retrieved is None
    
    async def test_get_invoices_with_filters(
        self,
        db_session,
        test_user,
        invoice_factory
    ):
        """Test getting invoices with filters"""
        # Create 3 invoices
        await InvoiceService.create_invoice(
            db_session,
            test_user.id,
            InvoiceCreate(**invoice_factory(
                invoice_number="INV-001",
                status="pending",
                amount=Decimal("1000.00")
            ))
        )
        await InvoiceService.create_invoice(
            db_session,
            test_user.id,
            InvoiceCreate(**invoice_factory(
                invoice_number="INV-002",
                status="paid",
                amount=Decimal("2000.00")
            ))
        )
        await InvoiceService.create_invoice(
            db_session,
            test_user.id,
            InvoiceCreate(**invoice_factory(
                invoice_number="INV-003",
                status="pending",
                amount=Decimal("3000.00")
            ))
        )
        await db_session.commit()
        
        # Filter by status
        filters = InvoiceFilter(status="pending")
        invoices, total = await InvoiceService.get_invoices(
            db_session,
            test_user.id,
            filters
        )
        
        assert total == 2
        assert all(inv.status == "pending" for inv in invoices)
    
    async def test_get_invoices_pagination(
        self,
        db_session,
        test_user,
        invoice_factory
    ):
        """Test invoice pagination"""
        # Create 5 invoices
        for i in range(5):
            await InvoiceService.create_invoice(
                db_session,
                test_user.id,
                InvoiceCreate(**invoice_factory(invoice_number=f"INV-{i}"))
            )
        await db_session.commit()
        
        # Get page 1 (2 items)
        filters = InvoiceFilter()
        invoices, total = await InvoiceService.get_invoices(
            db_session,
            test_user.id,
            filters,
            page=1,
            page_size=2
        )
        
        assert total == 5
        assert len(invoices) == 2
    
    async def test_update_invoice(
        self,
        db_session,
        test_user,
        invoice_factory
    ):
        """Test updating an invoice"""
        data = InvoiceCreate(**invoice_factory(
            amount=Decimal("1000.00"),
            tax_amount=Decimal("200.00")
        ))
        invoice = await InvoiceService.create_invoice(
            db_session,
            test_user.id,
            data
        )
        await db_session.commit()
        
        # Update invoice
        update_data = InvoiceUpdate(
            amount=Decimal("1500.00"),
            tax_amount=Decimal("300.00")
        )
        updated = await InvoiceService.update_invoice(
            db_session,
            invoice,
            update_data
        )
        await db_session.commit()
        
        assert updated.amount == Decimal("1500.00")
        assert updated.tax_amount == Decimal("300.00")
        assert updated.total_amount == Decimal("1800.00")
    
    async def test_mark_invoice_paid(
        self,
        db_session,
        test_user,
        invoice_factory
    ):
        """Test marking invoice as paid"""
        data = InvoiceCreate(**invoice_factory())
        invoice = await InvoiceService.create_invoice(
            db_session,
            test_user.id,
            data
        )
        await db_session.commit()
        
        # Mark as paid
        payment_date = date.today()
        paid_invoice = await InvoiceService.mark_invoice_paid(
            db_session,
            invoice,
            payment_date
        )
        await db_session.commit()
        
        assert paid_invoice.status == "paid"
        assert paid_invoice.payment_date == payment_date
    
    async def test_delete_invoice(
        self,
        db_session,
        test_user,
        invoice_factory
    ):
        """Test soft deleting an invoice"""
        data = InvoiceCreate(**invoice_factory())
        invoice = await InvoiceService.create_invoice(
            db_session,
            test_user.id,
            data
        )
        await db_session.commit()
        
        # Delete invoice
        await InvoiceService.delete_invoice(db_session, invoice)
        await db_session.commit()
        
        assert invoice.deleted_at is not None
        
        # Verify cannot retrieve
        retrieved = await InvoiceService.get_invoice(
            db_session,
            invoice.id,
            test_user.id
        )
        assert retrieved is None
    
    async def test_get_overdue_invoices(
        self,
        db_session,
        test_user,
        invoice_factory
    ):
        """Test getting overdue invoices"""
        # Create 1 overdue and 1 future invoice
        await InvoiceService.create_invoice(
            db_session,
            test_user.id,
            InvoiceCreate(**invoice_factory(
                invoice_number="INV-OVERDUE",
                due_date=date.today() - timedelta(days=5)
            ))
        )
        await InvoiceService.create_invoice(
            db_session,
            test_user.id,
            InvoiceCreate(**invoice_factory(
                invoice_number="INV-FUTURE",
                due_date=date.today() + timedelta(days=30)
            ))
        )
        await db_session.commit()
        
        # Get overdue
        overdue = await InvoiceService.get_overdue_invoices(
            db_session,
            test_user.id
        )
        
        assert len(overdue) == 1
        assert overdue[0].invoice_number == "INV-OVERDUE"


