"""
Unit tests for InvoiceService.
Tests all invoice operations including CRUD, filtering, and business logic.
Target: 100% code coverage
"""
import pytest
from datetime import date, timedelta, datetime
from decimal import Decimal
from uuid import uuid4

from app.services.invoice_service import InvoiceService
from app.schemas.invoice import InvoiceCreate, InvoiceUpdate, InvoiceFilter
from app.models.invoice import Invoice


# ============================================================================
# FIXTURES
# ============================================================================

@pytest.fixture
async def sample_invoice(db_session, test_user):
    """Create a sample invoice for testing."""
    invoice = Invoice(
        user_id=test_user.id,
        invoice_number="INV-2026-001",
        client_name="Test Client",
        client_email="client@example.com",
        client_address="123 Test St",
        amount=Decimal("1000.00"),
        tax_amount=Decimal("200.00"),
        total_amount=Decimal("1200.00"),
        currency="EUR",
        issue_date=date.today(),
        due_date=date.today() + timedelta(days=30),
        status="pending",
        is_reconciled=False,
        description="Test invoice",
        notes="Test notes"
    )
    db_session.add(invoice)
    await db_session.commit()
    await db_session.refresh(invoice)
    return invoice


@pytest.fixture
async def overdue_invoice(db_session, test_user):
    """Create an overdue invoice for testing."""
    invoice = Invoice(
        user_id=test_user.id,
        invoice_number="INV-2026-002",
        client_name="Overdue Client",
        client_email="overdue@example.com",
        amount=Decimal("500.00"),
        tax_amount=Decimal("100.00"),
        total_amount=Decimal("600.00"),
        currency="EUR",
        issue_date=date.today() - timedelta(days=60),
        due_date=date.today() - timedelta(days=30),
        status="pending",
        is_reconciled=False
    )
    db_session.add(invoice)
    await db_session.commit()
    await db_session.refresh(invoice)
    return invoice


# ============================================================================
# CREATE INVOICE TESTS
# ============================================================================

@pytest.mark.asyncio
@pytest.mark.unit
async def test_create_invoice_success(db_session, test_user):
    """Test successful invoice creation."""
    invoice_data = InvoiceCreate(
        invoice_number="INV-2026-100",
        client_name="New Client",
        client_email="new@example.com",
        client_address="456 New St",
        amount=Decimal("2000.00"),
        tax_amount=Decimal("400.00"),
        currency="EUR",
        issue_date=date.today(),
        due_date=date.today() + timedelta(days=30),
        description="New invoice",
        notes="Test notes"
    )
    
    invoice = await InvoiceService.create_invoice(
        db_session,
        test_user.id,
        invoice_data
    )
    
    assert invoice.id is not None
    assert invoice.user_id == test_user.id
    assert invoice.invoice_number == "INV-2026-100"
    assert invoice.client_name == "New Client"
    assert invoice.amount == Decimal("2000.00")
    assert invoice.tax_amount == Decimal("400.00")
    assert invoice.total_amount == Decimal("2400.00")
    assert invoice.status == "pending"
    assert invoice.is_reconciled is False


@pytest.mark.asyncio
@pytest.mark.unit
async def test_create_invoice_calculates_total(db_session, test_user):
    """Test that total amount is calculated correctly."""
    invoice_data = InvoiceCreate(
        invoice_number="INV-2026-101",
        client_name="Math Client",
        amount=Decimal("1500.50"),
        tax_amount=Decimal("300.10"),
        currency="EUR",
        issue_date=date.today(),
        due_date=date.today() + timedelta(days=30)
    )
    
    invoice = await InvoiceService.create_invoice(
        db_session,
        test_user.id,
        invoice_data
    )
    
    assert invoice.total_amount == Decimal("1800.60")


@pytest.mark.asyncio
@pytest.mark.unit
async def test_create_invoice_status_overdue_when_past_due(db_session, test_user):
    """Test that invoice is marked overdue if due_date is in the past."""
    invoice_data = InvoiceCreate(
        invoice_number="INV-2026-102",
        client_name="Late Client",
        amount=Decimal("500.00"),
        tax_amount=Decimal("0.00"),
        currency="EUR",
        issue_date=date.today() - timedelta(days=60),
        due_date=date.today() - timedelta(days=1)  # Yesterday
    )
    
    invoice = await InvoiceService.create_invoice(
        db_session,
        test_user.id,
        invoice_data
    )
    
    assert invoice.status == "overdue"


@pytest.mark.asyncio
@pytest.mark.unit
async def test_create_invoice_duplicate_number(db_session, test_user, sample_invoice):
    """Test that duplicate invoice number raises error."""
    invoice_data = InvoiceCreate(
        invoice_number=sample_invoice.invoice_number,  # Duplicate
        client_name="Duplicate Client",
        amount=Decimal("100.00"),
        tax_amount=Decimal("0.00"),
        currency="EUR",
        issue_date=date.today(),
        due_date=date.today() + timedelta(days=30)
    )
    
    with pytest.raises(ValueError, match="already exists"):
        await InvoiceService.create_invoice(
            db_session,
            test_user.id,
            invoice_data
        )


@pytest.mark.asyncio
@pytest.mark.unit
async def test_create_invoice_different_users_same_number(db_session, test_user, test_user_unverified):
    """Test that different users can have same invoice number."""
    # User 1 creates invoice
    invoice_data_1 = InvoiceCreate(
        invoice_number="INV-SHARED-001",
        client_name="Client 1",
        amount=Decimal("100.00"),
        tax_amount=Decimal("0.00"),
        currency="EUR",
        issue_date=date.today(),
        due_date=date.today() + timedelta(days=30)
    )
    invoice1 = await InvoiceService.create_invoice(
        db_session,
        test_user.id,
        invoice_data_1
    )
    
    # User 2 creates invoice with same number (should work)
    invoice_data_2 = InvoiceCreate(
        invoice_number="INV-SHARED-001",
        client_name="Client 2",
        amount=Decimal("200.00"),
        tax_amount=Decimal("0.00"),
        currency="EUR",
        issue_date=date.today(),
        due_date=date.today() + timedelta(days=30)
    )
    invoice2 = await InvoiceService.create_invoice(
        db_session,
        test_user_unverified.id,
        invoice_data_2
    )
    
    assert invoice1.invoice_number == invoice2.invoice_number
    assert invoice1.user_id != invoice2.user_id


# ============================================================================
# GET INVOICE TESTS
# ============================================================================

@pytest.mark.asyncio
@pytest.mark.unit
async def test_get_invoice_success(db_session, test_user, sample_invoice):
    """Test successful invoice retrieval."""
    invoice = await InvoiceService.get_invoice(
        db_session,
        sample_invoice.id,
        test_user.id
    )
    
    assert invoice is not None
    assert invoice.id == sample_invoice.id
    assert invoice.invoice_number == sample_invoice.invoice_number


@pytest.mark.asyncio
@pytest.mark.unit
async def test_get_invoice_not_found(db_session, test_user):
    """Test get_invoice returns None for non-existent invoice."""
    invoice = await InvoiceService.get_invoice(
        db_session,
        uuid4(),  # Random UUID
        test_user.id
    )
    
    assert invoice is None


@pytest.mark.asyncio
@pytest.mark.unit
async def test_get_invoice_wrong_user(db_session, test_user, test_user_unverified, sample_invoice):
    """Test that user cannot access another user's invoice."""
    invoice = await InvoiceService.get_invoice(
        db_session,
        sample_invoice.id,
        test_user_unverified.id  # Different user
    )
    
    assert invoice is None


@pytest.mark.asyncio
@pytest.mark.unit
async def test_get_invoice_ignores_deleted(db_session, test_user, sample_invoice):
    """Test that deleted invoices are not returned."""
    # Soft delete invoice
    sample_invoice.deleted_at = datetime.utcnow()
    await db_session.commit()
    
    invoice = await InvoiceService.get_invoice(
        db_session,
        sample_invoice.id,
        test_user.id
    )
    
    assert invoice is None


# ============================================================================
# GET INVOICES (LIST + FILTER) TESTS
# ============================================================================

@pytest.mark.asyncio
@pytest.mark.unit
async def test_get_invoices_no_filters(db_session, test_user, sample_invoice, overdue_invoice):
    """Test getting invoices without filters."""
    filters = InvoiceFilter()
    
    invoices, total = await InvoiceService.get_invoices(
        db_session,
        test_user.id,
        filters,
        page=1,
        page_size=50
    )
    
    assert len(invoices) == 2
    assert total == 2
    assert all(inv.user_id == test_user.id for inv in invoices)


@pytest.mark.asyncio
@pytest.mark.unit
async def test_get_invoices_filter_by_status(db_session, test_user, sample_invoice):
    """Test filtering invoices by status."""
    filters = InvoiceFilter(status="pending")
    
    invoices, total = await InvoiceService.get_invoices(
        db_session,
        test_user.id,
        filters
    )
    
    assert all(inv.status == "pending" for inv in invoices)


@pytest.mark.asyncio
@pytest.mark.unit
async def test_get_invoices_filter_by_client_name(db_session, test_user, sample_invoice, overdue_invoice):
    """Test filtering invoices by client name (partial match)."""
    filters = InvoiceFilter(client_name="Test")
    
    invoices, total = await InvoiceService.get_invoices(
        db_session,
        test_user.id,
        filters
    )
    
    assert len(invoices) == 1
    assert invoices[0].client_name == "Test Client"


@pytest.mark.asyncio
@pytest.mark.unit
async def test_get_invoices_filter_by_date_range(db_session, test_user, sample_invoice, overdue_invoice):
    """Test filtering invoices by date range."""
    filters = InvoiceFilter(
        start_date=date.today(),
        end_date=date.today() + timedelta(days=60)
    )
    
    invoices, total = await InvoiceService.get_invoices(
        db_session,
        test_user.id,
        filters
    )
    
    # Should only get sample_invoice (due_date=today+30 is in range)
    # overdue_invoice (due_date=today-30) is NOT in range
    assert len(invoices) == 1
    assert invoices[0].id == sample_invoice.id


@pytest.mark.asyncio
@pytest.mark.unit
async def test_get_invoices_filter_by_amount_range(db_session, test_user, sample_invoice, overdue_invoice):
    """Test filtering invoices by amount range."""
    filters = InvoiceFilter(
        min_amount=Decimal("1000.00"),
        max_amount=Decimal("2000.00")
    )
    
    invoices, total = await InvoiceService.get_invoices(
        db_session,
        test_user.id,
        filters
    )
    
    # Should only get sample_invoice (total_amount=1200)
    assert len(invoices) == 1
    assert invoices[0].id == sample_invoice.id


@pytest.mark.asyncio
@pytest.mark.unit
async def test_get_invoices_filter_by_reconciled(db_session, test_user, sample_invoice):
    """Test filtering invoices by reconciliation status."""
    filters = InvoiceFilter(is_reconciled=False)
    
    invoices, total = await InvoiceService.get_invoices(
        db_session,
        test_user.id,
        filters
    )
    
    assert all(not inv.is_reconciled for inv in invoices)


@pytest.mark.asyncio
@pytest.mark.unit
async def test_get_invoices_pagination(db_session, test_user):
    """Test invoice pagination."""
    # Create 10 invoices
    for i in range(10):
        invoice_data = InvoiceCreate(
            invoice_number=f"INV-PAGE-{i:03d}",
            client_name=f"Client {i}",
            amount=Decimal("100.00"),
            tax_amount=Decimal("0.00"),
            currency="EUR",
            issue_date=date.today(),
            due_date=date.today() + timedelta(days=30)
        )
        await InvoiceService.create_invoice(db_session, test_user.id, invoice_data)
    
    await db_session.commit()
    
    filters = InvoiceFilter()
    
    # Page 1
    invoices_p1, total = await InvoiceService.get_invoices(
        db_session,
        test_user.id,
        filters,
        page=1,
        page_size=5
    )
    
    assert len(invoices_p1) == 5
    assert total == 10
    
    # Page 2
    invoices_p2, _ = await InvoiceService.get_invoices(
        db_session,
        test_user.id,
        filters,
        page=2,
        page_size=5
    )
    
    assert len(invoices_p2) == 5
    assert invoices_p1[0].id != invoices_p2[0].id


@pytest.mark.asyncio
@pytest.mark.unit
async def test_get_invoices_empty_result(db_session, test_user):
    """Test get_invoices with no matching invoices."""
    filters = InvoiceFilter(status="paid")  # No paid invoices
    
    invoices, total = await InvoiceService.get_invoices(
        db_session,
        test_user.id,
        filters
    )
    
    assert len(invoices) == 0
    assert total == 0


# ============================================================================
# UPDATE INVOICE TESTS
# ============================================================================

@pytest.mark.asyncio
@pytest.mark.unit
async def test_update_invoice_basic_fields(db_session, sample_invoice):
    """Test updating basic invoice fields."""
    update_data = InvoiceUpdate(
        client_name="Updated Client Name",
        notes="Updated notes"
    )
    
    updated = await InvoiceService.update_invoice(
        db_session,
        sample_invoice,
        update_data
    )
    
    assert updated.client_name == "Updated Client Name"
    assert updated.notes == "Updated notes"
    # Original fields unchanged
    assert updated.amount == sample_invoice.amount


@pytest.mark.asyncio
@pytest.mark.unit
async def test_update_invoice_recalculates_total(db_session, sample_invoice):
    """Test that updating amount recalculates total."""
    original_total = sample_invoice.total_amount
    
    update_data = InvoiceUpdate(
        amount=Decimal("1500.00")  # Change amount
    )
    
    updated = await InvoiceService.update_invoice(
        db_session,
        sample_invoice,
        update_data
    )
    
    # Total should be recalculated (1500 + 200 tax)
    assert updated.total_amount == Decimal("1700.00")
    assert updated.total_amount != original_total


@pytest.mark.asyncio
@pytest.mark.unit
async def test_update_invoice_tax_recalculates_total(db_session, sample_invoice):
    """Test that updating tax_amount recalculates total."""
    update_data = InvoiceUpdate(
        tax_amount=Decimal("300.00")  # Change tax
    )
    
    updated = await InvoiceService.update_invoice(
        db_session,
        sample_invoice,
        update_data
    )
    
    # Total should be recalculated (1000 amount + 300 tax)
    assert updated.total_amount == Decimal("1300.00")


@pytest.mark.asyncio
@pytest.mark.unit
async def test_update_invoice_status(db_session, sample_invoice):
    """Test updating invoice status."""
    update_data = InvoiceUpdate(status="cancelled")
    
    updated = await InvoiceService.update_invoice(
        db_session,
        sample_invoice,
        update_data
    )
    
    assert updated.status == "cancelled"


# ============================================================================
# MARK INVOICE PAID TESTS
# ============================================================================

@pytest.mark.asyncio
@pytest.mark.unit
async def test_mark_invoice_paid(db_session, sample_invoice):
    """Test marking invoice as paid."""
    payment_date = date.today()
    
    updated = await InvoiceService.mark_invoice_paid(
        db_session,
        sample_invoice,
        payment_date
    )
    
    assert updated.status == "paid"
    assert updated.payment_date == payment_date


@pytest.mark.asyncio
@pytest.mark.unit
async def test_mark_invoice_paid_past_date(db_session, sample_invoice):
    """Test marking invoice paid with past payment date."""
    payment_date = date.today() - timedelta(days=10)
    
    updated = await InvoiceService.mark_invoice_paid(
        db_session,
        sample_invoice,
        payment_date
    )
    
    assert updated.status == "paid"
    assert updated.payment_date == payment_date


# ============================================================================
# DELETE INVOICE TESTS
# ============================================================================

@pytest.mark.asyncio
@pytest.mark.unit
async def test_delete_invoice(db_session, test_user, sample_invoice):
    """Test soft deleting invoice."""
    await InvoiceService.delete_invoice(db_session, sample_invoice)
    await db_session.commit()
    
    # Invoice should have deleted_at timestamp
    await db_session.refresh(sample_invoice)
    assert sample_invoice.deleted_at is not None
    
    # Invoice should not be retrievable
    retrieved = await InvoiceService.get_invoice(
        db_session,
        sample_invoice.id,
        test_user.id
    )
    assert retrieved is None


# ============================================================================
# GET OVERDUE INVOICES TESTS
# ============================================================================

@pytest.mark.asyncio
@pytest.mark.unit
async def test_get_overdue_invoices_for_user(db_session, test_user, overdue_invoice):
    """Test getting overdue invoices for specific user."""
    overdue = await InvoiceService.get_overdue_invoices(
        db_session,
        user_id=test_user.id
    )
    
    assert len(overdue) == 1
    assert overdue[0].id == overdue_invoice.id
    assert overdue[0].due_date < date.today()
    assert overdue[0].status == "pending"


@pytest.mark.asyncio
@pytest.mark.unit
async def test_get_overdue_invoices_all_users(db_session, test_user, test_user_unverified, overdue_invoice):
    """Test getting overdue invoices for all users."""
    # Create overdue invoice for second user
    invoice_data = InvoiceCreate(
        invoice_number="INV-USER2-001",
        client_name="Client 2",
        amount=Decimal("300.00"),
        tax_amount=Decimal("0.00"),
        currency="EUR",
        issue_date=date.today() - timedelta(days=40),
        due_date=date.today() - timedelta(days=10)
    )
    await InvoiceService.create_invoice(
        db_session,
        test_user_unverified.id,
        invoice_data
    )
    await db_session.commit()
    
    overdue = await InvoiceService.get_overdue_invoices(db_session)
    
    # Should get both users' overdue invoices
    assert len(overdue) >= 2


@pytest.mark.asyncio
@pytest.mark.unit
async def test_get_overdue_invoices_excludes_paid(db_session, test_user, overdue_invoice):
    """Test that paid invoices are not included in overdue list."""
    # Mark as paid
    await InvoiceService.mark_invoice_paid(
        db_session,
        overdue_invoice,
        date.today()
    )
    await db_session.commit()
    
    overdue = await InvoiceService.get_overdue_invoices(
        db_session,
        user_id=test_user.id
    )
    
    assert len(overdue) == 0


@pytest.mark.asyncio
@pytest.mark.unit
async def test_get_overdue_invoices_excludes_deleted(db_session, test_user, overdue_invoice):
    """Test that deleted invoices are not included."""
    # Delete invoice
    await InvoiceService.delete_invoice(db_session, overdue_invoice)
    await db_session.commit()
    
    overdue = await InvoiceService.get_overdue_invoices(
        db_session,
        user_id=test_user.id
    )
    
    assert len(overdue) == 0


@pytest.mark.asyncio
@pytest.mark.unit
async def test_get_overdue_invoices_ordered_by_date(db_session, test_user):
    """Test that overdue invoices are ordered by due_date ascending."""
    # Create multiple overdue invoices
    for i in range(3):
        invoice_data = InvoiceCreate(
            invoice_number=f"INV-ORDER-{i:03d}",
            client_name=f"Client {i}",
            amount=Decimal("100.00"),
            tax_amount=Decimal("0.00"),
            currency="EUR",
            issue_date=date.today() - timedelta(days=60 - i*10),
            due_date=date.today() - timedelta(days=30 - i*10)
        )
        await InvoiceService.create_invoice(db_session, test_user.id, invoice_data)
    
    await db_session.commit()
    
    overdue = await InvoiceService.get_overdue_invoices(
        db_session,
        user_id=test_user.id
    )
    
    # Check order (oldest due_date first)
    assert len(overdue) == 3
    for i in range(len(overdue) - 1):
        assert overdue[i].due_date <= overdue[i + 1].due_date

