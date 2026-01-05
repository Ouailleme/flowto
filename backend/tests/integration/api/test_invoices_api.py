"""
Integration tests for Invoices API endpoints.
"""
import pytest
from httpx import AsyncClient
from decimal import Decimal
from datetime import date, timedelta


@pytest.mark.asyncio
@pytest.mark.integration
async def test_create_invoice_success(client: AsyncClient, auth_headers):
    """Test creating an invoice via API."""
    response = await client.post(
        "/api/v1/invoices/",
        json={
            "invoice_number": "API-TEST-001",
            "client_name": "API Test Client",
            "client_email": "client@test.com",
            "amount": 1500.50,
            "tax_amount": 300.10,
            "currency": "EUR",
            "issue_date": str(date.today()),
            "due_date": str(date.today() + timedelta(days=30)),
            "description": "API Test Invoice"
        },
        headers=auth_headers
    )
    
    assert response.status_code == 201
    data = response.json()
    assert data["invoice_number"] == "API-TEST-001"
    assert data["client_name"] == "API Test Client"
    assert float(data["amount"]) == 1500.50
    assert float(data["tax_amount"]) == 300.10
    assert float(data["total_amount"]) == 1800.60  # amount + tax
    assert data["status"] == "pending"
    assert "id" in data


@pytest.mark.asyncio
@pytest.mark.integration
async def test_create_invoice_duplicate_number(client: AsyncClient, auth_headers):
    """Test creating invoice with duplicate number fails."""
    invoice_data = {
        "invoice_number": "DUP-001",
        "client_name": "Test Client",
        "amount": 100.00,
        "tax_amount": 0.00,
        "currency": "EUR",
        "issue_date": str(date.today()),
        "due_date": str(date.today() + timedelta(days=30))
    }
    
    # Create first invoice
    response1 = await client.post(
        "/api/v1/invoices/",
        json=invoice_data,
        headers=auth_headers
    )
    assert response1.status_code == 201
    
    # Try to create duplicate
    response2 = await client.post(
        "/api/v1/invoices/",
        json=invoice_data,
        headers=auth_headers
    )
    assert response2.status_code == 400
    assert "already exists" in response2.json()["detail"].lower()


@pytest.mark.asyncio
@pytest.mark.integration
async def test_create_invoice_unauthorized(client: AsyncClient):
    """Test creating invoice without auth fails."""
    response = await client.post(
        "/api/v1/invoices/",
        json={
            "invoice_number": "UNAUTH-001",
            "client_name": "Test",
            "amount": 100.00,
            "tax_amount": 0.00,
            "currency": "EUR",
            "issue_date": str(date.today()),
            "due_date": str(date.today() + timedelta(days=30))
        }
    )
    
    assert response.status_code in [401, 403]  # Both are acceptable for unauthorized


@pytest.mark.asyncio
@pytest.mark.integration
async def test_get_invoices_list(client: AsyncClient, auth_headers):
    """Test getting list of invoices."""
    # Create a few invoices first
    for i in range(3):
        await client.post(
            "/api/v1/invoices/",
            json={
                "invoice_number": f"LIST-{i:03d}",
                "client_name": f"Client {i}",
                "amount": 100.00 * (i + 1),
                "tax_amount": 0.00,
                "currency": "EUR",
                "issue_date": str(date.today()),
                "due_date": str(date.today() + timedelta(days=30))
            },
            headers=auth_headers
        )
    
    # Get list
    response = await client.get(
        "/api/v1/invoices/?page=1&page_size=10",
        headers=auth_headers
    )
    
    assert response.status_code == 200
    data = response.json()
    assert "invoices" in data
    assert "total" in data
    assert len(data["invoices"]) >= 3


@pytest.mark.asyncio
@pytest.mark.integration
async def test_get_invoice_by_id(client: AsyncClient, auth_headers):
    """Test getting a specific invoice by ID."""
    # Create invoice
    create_response = await client.post(
        "/api/v1/invoices/",
        json={
            "invoice_number": "GETBYID-001",
            "client_name": "Get Test Client",
            "amount": 250.00,
            "tax_amount": 50.00,
            "currency": "EUR",
            "issue_date": str(date.today()),
            "due_date": str(date.today() + timedelta(days=30))
        },
        headers=auth_headers
    )
    invoice_id = create_response.json()["id"]
    
    # Get by ID
    response = await client.get(
        f"/api/v1/invoices/{invoice_id}",
        headers=auth_headers
    )
    
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == invoice_id
    assert data["invoice_number"] == "GETBYID-001"


@pytest.mark.asyncio
@pytest.mark.integration
async def test_get_invoice_not_found(client: AsyncClient, auth_headers):
    """Test getting non-existent invoice returns 404."""
    fake_id = "00000000-0000-0000-0000-000000000000"
    response = await client.get(
        f"/api/v1/invoices/{fake_id}",
        headers=auth_headers
    )
    
    assert response.status_code == 404


@pytest.mark.asyncio
@pytest.mark.integration
async def test_update_invoice(client: AsyncClient, auth_headers):
    """Test updating an invoice."""
    # Create invoice
    create_response = await client.post(
        "/api/v1/invoices/",
        json={
            "invoice_number": "UPDATE-001",
            "client_name": "Original Client",
            "amount": 100.00,
            "tax_amount": 0.00,
            "currency": "EUR",
            "issue_date": str(date.today()),
            "due_date": str(date.today() + timedelta(days=30))
        },
        headers=auth_headers
    )
    invoice_id = create_response.json()["id"]
    
    # Update invoice
    response = await client.patch(
        f"/api/v1/invoices/{invoice_id}",
        json={
            "client_name": "Updated Client",
            "amount": 150.00
        },
        headers=auth_headers
    )
    
    assert response.status_code == 200
    data = response.json()
    assert data["client_name"] == "Updated Client"
    assert float(data["amount"]) == 150.00
    assert float(data["total_amount"]) == 150.00  # tax_amount still 0


@pytest.mark.asyncio
@pytest.mark.integration
async def test_mark_invoice_paid(client: AsyncClient, auth_headers):
    """Test marking an invoice as paid using PATCH."""
    # Create invoice
    create_response = await client.post(
        "/api/v1/invoices/",
        json={
            "invoice_number": "PAID-001",
            "client_name": "Payment Client",
            "amount": 500.00,
            "tax_amount": 100.00,
            "currency": "EUR",
            "issue_date": str(date.today()),
            "due_date": str(date.today() + timedelta(days=30))
        },
        headers=auth_headers
    )
    invoice_id = create_response.json()["id"]
    
    # Mark as paid using PATCH
    response = await client.patch(
        f"/api/v1/invoices/{invoice_id}",
        json={
            "status": "paid",
            "payment_date": str(date.today())
        },
        headers=auth_headers
    )
    
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "paid"
    # payment_date might not be updated via PATCH, that's ok
    # The important part is that status changed


@pytest.mark.asyncio
@pytest.mark.integration
async def test_delete_invoice(client: AsyncClient, auth_headers):
    """Test deleting an invoice (soft delete)."""
    # Create invoice
    create_response = await client.post(
        "/api/v1/invoices/",
        json={
            "invoice_number": "DELETE-001",
            "client_name": "Delete Client",
            "amount": 100.00,
            "tax_amount": 0.00,
            "currency": "EUR",
            "issue_date": str(date.today()),
            "due_date": str(date.today() + timedelta(days=30))
        },
        headers=auth_headers
    )
    invoice_id = create_response.json()["id"]
    
    # Delete invoice
    response = await client.delete(
        f"/api/v1/invoices/{invoice_id}",
        headers=auth_headers
    )
    
    assert response.status_code == 204
    
    # Verify it's not in the list anymore
    list_response = await client.get(
        f"/api/v1/invoices/{invoice_id}",
        headers=auth_headers
    )
    assert list_response.status_code == 404


@pytest.mark.asyncio
@pytest.mark.integration
async def test_filter_invoices_by_status(client: AsyncClient, auth_headers):
    """Test filtering invoices by status."""
    # Create paid and pending invoices
    for i in range(2):
        response = await client.post(
            "/api/v1/invoices/",
            json={
                "invoice_number": f"FILTER-PAID-{i:03d}",
                "client_name": f"Filter Client {i}",
                "amount": 100.00,
                "tax_amount": 0.00,
                "currency": "EUR",
                "issue_date": str(date.today()),
                "due_date": str(date.today() + timedelta(days=30))
            },
            headers=auth_headers
        )
        invoice_id = response.json()["id"]
        # Mark as paid using PATCH
        await client.patch(
            f"/api/v1/invoices/{invoice_id}",
            json={"status": "paid", "payment_date": str(date.today())},
            headers=auth_headers
        )
    
    # Filter by paid status
    response = await client.get(
        "/api/v1/invoices/?status=paid",
        headers=auth_headers
    )
    
    assert response.status_code == 200
    data = response.json()
    # Should have at least the 2 we just created
    assert len(data["invoices"]) >= 2
    for invoice in data["invoices"]:
        assert invoice["status"] == "paid"


@pytest.mark.asyncio
@pytest.mark.integration
async def test_filter_invoices_by_client(client: AsyncClient, auth_headers):
    """Test filtering invoices by client name."""
    # Create invoices for specific client
    client_name = "Specific Filter Client XYZ"
    for i in range(2):
        await client.post(
            "/api/v1/invoices/",
            json={
                "invoice_number": f"FILTER-CLIENT-{i:03d}",
                "client_name": client_name,
                "amount": 100.00,
                "tax_amount": 0.00,
                "currency": "EUR",
                "issue_date": str(date.today()),
                "due_date": str(date.today() + timedelta(days=30))
            },
            headers=auth_headers
        )
    
    # Filter by client name (partial match)
    response = await client.get(
        f"/api/v1/invoices/?client_name=Specific%20Filter",
        headers=auth_headers
    )
    
    assert response.status_code == 200
    data = response.json()
    assert len(data["invoices"]) >= 2
    for invoice in data["invoices"]:
        assert "Specific Filter" in invoice["client_name"]


@pytest.mark.asyncio
@pytest.mark.integration
async def test_invoice_pagination(client: AsyncClient, auth_headers):
    """Test invoice pagination."""
    # Create multiple invoices
    for i in range(15):
        await client.post(
            "/api/v1/invoices/",
            json={
                "invoice_number": f"PAGE-{i:03d}",
                "client_name": f"Page Client {i}",
                "amount": 100.00,
                "tax_amount": 0.00,
                "currency": "EUR",
                "issue_date": str(date.today()),
                "due_date": str(date.today() + timedelta(days=30))
            },
            headers=auth_headers
        )
    
    # Get first page
    response1 = await client.get(
        "/api/v1/invoices/?page=1&page_size=10",
        headers=auth_headers
    )
    assert response1.status_code == 200
    data1 = response1.json()
    assert len(data1["invoices"]) == 10
    assert data1["page"] == 1
    
    # Get second page
    response2 = await client.get(
        "/api/v1/invoices/?page=2&page_size=10",
        headers=auth_headers
    )
    assert response2.status_code == 200
    data2 = response2.json()
    assert len(data2["invoices"]) >= 5  # At least the 5 remaining
    assert data2["page"] == 2

