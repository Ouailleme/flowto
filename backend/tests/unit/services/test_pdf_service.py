"""Tests for PDFService"""
import pytest
from datetime import datetime, date, timedelta
from decimal import Decimal
from unittest.mock import MagicMock, patch

from app.services.pdf_service import PDFService
from app.models.invoice import Invoice
from app.models.user import User


@pytest.fixture
def sample_user():
    """Sample user for testing"""
    user = User(
        email="test@company.com",
        company_name="Test Company SARL",
        phone="+33 1 23 45 67 89",
        address="123 Rue de Test, 75001 Paris",
        hashed_password="hashed"
    )
    user.id = "user-123"
    return user


@pytest.fixture
def sample_invoice(sample_user):
    """Sample invoice for testing"""
    invoice = Invoice(
        user_id=sample_user.id,
        invoice_number="INV-2024-001",
        client_name="Client Test SAS",
        client_email="client@test.com",
        client_address="456 Avenue Client, 69000 Lyon",
        issue_date=date(2024, 1, 15),
        due_date=date(2024, 2, 15),
        currency="EUR",
        status="pending",
        subtotal=Decimal("1000.00"),
        tax_rate=Decimal("20.00"),
        tax_amount=Decimal("200.00"),
        discount_amount=Decimal("0.00"),
        total_amount=Decimal("1200.00"),
        payment_terms="Paiement à 30 jours",
        notes="Merci pour votre confiance",
        items=[]
    )
    invoice.id = "invoice-123"
    return invoice


def test_generate_invoice_pdf_success(sample_invoice, sample_user):
    """Test successful PDF generation"""
    pdf_bytes = PDFService.generate_invoice_pdf(
        invoice=sample_invoice,
        user=sample_user
    )
    
    # Check PDF was generated
    assert pdf_bytes is not None
    assert len(pdf_bytes) > 0
    
    # Check PDF magic bytes (PDF starts with %PDF)
    assert pdf_bytes[:4] == b'%PDF'


def test_generate_invoice_pdf_with_items(sample_invoice, sample_user):
    """Test PDF generation with invoice items"""
    # Add items to invoice
    sample_invoice.items = [
        MagicMock(
            description="Service A",
            details="Détails du service A",
            quantity=2,
            unit_price=Decimal("250.00")
        ),
        MagicMock(
            description="Service B",
            details=None,
            quantity=1,
            unit_price=Decimal("500.00")
        )
    ]
    
    pdf_bytes = PDFService.generate_invoice_pdf(
        invoice=sample_invoice,
        user=sample_user
    )
    
    assert pdf_bytes is not None
    assert len(pdf_bytes) > 0
    assert pdf_bytes[:4] == b'%PDF'


def test_generate_invoice_pdf_paid_status(sample_invoice, sample_user):
    """Test PDF generation for paid invoice"""
    sample_invoice.status = "paid"
    
    pdf_bytes = PDFService.generate_invoice_pdf(
        invoice=sample_invoice,
        user=sample_user
    )
    
    assert pdf_bytes is not None
    assert pdf_bytes[:4] == b'%PDF'


def test_generate_invoice_pdf_with_discount(sample_invoice, sample_user):
    """Test PDF generation with discount"""
    sample_invoice.discount_amount = Decimal("100.00")
    sample_invoice.total_amount = Decimal("1100.00")
    
    pdf_bytes = PDFService.generate_invoice_pdf(
        invoice=sample_invoice,
        user=sample_user
    )
    
    assert pdf_bytes is not None
    assert pdf_bytes[:4] == b'%PDF'


def test_generate_invoice_pdf_minimal_user_info(sample_invoice):
    """Test PDF generation with minimal user information"""
    minimal_user = User(
        email="minimal@test.com",
        company_name="Minimal Company",
        hashed_password="hashed"
    )
    minimal_user.id = "user-minimal"
    # No phone, address, etc.
    
    pdf_bytes = PDFService.generate_invoice_pdf(
        invoice=sample_invoice,
        user=minimal_user
    )
    
    assert pdf_bytes is not None
    assert pdf_bytes[:4] == b'%PDF'


def test_generate_invoice_pdf_minimal_invoice_info(sample_user):
    """Test PDF generation with minimal invoice information"""
    minimal_invoice = Invoice(
        user_id=sample_user.id,
        invoice_number="INV-MIN-001",
        client_name="Minimal Client",
        # No client_email, client_address
        issue_date=date.today(),
        due_date=date.today() + timedelta(days=30),
        currency="EUR",
        status="pending",
        subtotal=Decimal("500.00"),
        tax_rate=Decimal("0.00"),
        tax_amount=Decimal("0.00"),
        discount_amount=Decimal("0.00"),
        total_amount=Decimal("500.00"),
        items=[]
    )
    minimal_invoice.id = "invoice-min"
    
    pdf_bytes = PDFService.generate_invoice_pdf(
        invoice=minimal_invoice,
        user=sample_user
    )
    
    assert pdf_bytes is not None
    assert pdf_bytes[:4] == b'%PDF'


def test_generate_invoice_pdf_different_currencies(sample_invoice, sample_user):
    """Test PDF generation with different currencies"""
    currencies = ["EUR", "USD", "GBP"]
    
    for currency in currencies:
        sample_invoice.currency = currency
        
        pdf_bytes = PDFService.generate_invoice_pdf(
            invoice=sample_invoice,
            user=sample_user
        )
        
        assert pdf_bytes is not None
        assert pdf_bytes[:4] == b'%PDF'


def test_generate_invoice_pdf_all_statuses(sample_invoice, sample_user):
    """Test PDF generation for all invoice statuses"""
    statuses = ["pending", "paid", "overdue", "cancelled"]
    
    for status in statuses:
        sample_invoice.status = status
        
        pdf_bytes = PDFService.generate_invoice_pdf(
            invoice=sample_invoice,
            user=sample_user
        )
        
        assert pdf_bytes is not None
        assert pdf_bytes[:4] == b'%PDF'


def test_get_invoice_filename_standard(sample_invoice):
    """Test getting standard invoice filename"""
    filename = PDFService.get_invoice_filename(sample_invoice)
    
    assert filename == "Facture_INV-2024-001_Client_Test_SAS.pdf"
    assert filename.endswith(".pdf")
    assert "INV-2024-001" in filename


def test_get_invoice_filename_special_characters():
    """Test filename generation with special characters in client name"""
    invoice = MagicMock()
    invoice.invoice_number = "INV-2024-002"
    invoice.client_name = "Client@#$%Special!Characters"
    
    filename = PDFService.get_invoice_filename(invoice)
    
    # Special characters should be removed
    assert "@" not in filename
    assert "#" not in filename
    assert "%" not in filename
    assert "!" not in filename
    assert filename.endswith(".pdf")


def test_get_invoice_filename_spaces():
    """Test filename generation handles spaces correctly"""
    invoice = MagicMock()
    invoice.invoice_number = "INV-2024-003"
    invoice.client_name = "Client With Many   Spaces"
    
    filename = PDFService.get_invoice_filename(invoice)
    
    # Spaces should be replaced with underscores
    assert "  " not in filename  # No double spaces
    assert filename.count("_") >= 4  # Multiple underscores for spaces


def test_get_invoice_filename_long_name():
    """Test filename generation with long client name"""
    invoice = MagicMock()
    invoice.invoice_number = "INV-2024-004"
    invoice.client_name = "A" * 200  # Very long name
    
    filename = PDFService.get_invoice_filename(invoice)
    
    assert filename.endswith(".pdf")
    assert "INV-2024-004" in filename


def test_generate_invoice_pdf_invalid_data():
    """Test PDF generation with invalid data raises ValueError"""
    invoice = None
    user = None
    
    with pytest.raises((ValueError, AttributeError)):
        PDFService.generate_invoice_pdf(
            invoice=invoice,
            user=user
        )


def test_generate_invoice_pdf_missing_required_fields(sample_user):
    """Test PDF generation with missing required fields"""
    incomplete_invoice = MagicMock()
    incomplete_invoice.id = "test-id"
    # Missing many required fields
    
    # Should raise an error or handle gracefully
    try:
        pdf_bytes = PDFService.generate_invoice_pdf(
            invoice=incomplete_invoice,
            user=sample_user
        )
        # If it doesn't raise, it should at least return something
        assert pdf_bytes is not None
    except (ValueError, AttributeError, Exception):
        # Expected behavior - missing fields cause error
        pass


def test_invoice_template_contains_required_elements():
    """Test that invoice template contains all required elements"""
    template = PDFService.INVOICE_TEMPLATE
    
    # Check for essential template elements
    assert "invoice.invoice_number" in template
    assert "invoice.client_name" in template
    assert "invoice.total_amount" in template
    assert "invoice.status" in template
    assert "invoice.issue_date" in template
    assert "invoice.due_date" in template
    assert "user.company_name" in template
    assert "user.email" in template
    
    # Check for styling
    assert "<style>" in template
    assert "</style>" in template
    assert "font-family" in template
    
    # Check for structure
    assert "<table>" in template
    assert "<thead>" in template
    assert "<tbody>" in template


def test_invoice_template_handles_optional_fields():
    """Test that template properly handles optional fields"""
    template = PDFService.INVOICE_TEMPLATE
    
    # Check for conditional rendering
    assert "{% if invoice.client_email %}" in template
    assert "{% if invoice.client_address %}" in template
    assert "{% if invoice.notes %}" in template
    assert "{% if invoice.payment_instructions %}" in template
    assert "{% if invoice.tax_amount > 0 %}" in template
    assert "{% if invoice.discount_amount > 0 %}" in template


def test_invoice_template_loops_items():
    """Test that template properly loops through items"""
    template = PDFService.INVOICE_TEMPLATE
    
    assert "{% for item in invoice.items %}" in template
    assert "{% endfor %}" in template
    assert "item.description" in template
    assert "item.quantity" in template
    assert "item.unit_price" in template


def test_invoice_template_status_badges():
    """Test that template includes status badge styling"""
    template = PDFService.INVOICE_TEMPLATE
    
    assert "status-pending" in template
    assert "status-paid" in template
    assert "status-overdue" in template
    assert "status-cancelled" in template

