"""Integration tests for Invoice API endpoints"""
import pytest
from datetime import date, timedelta
from decimal import Decimal


@pytest.mark.asyncio
class TestInvoiceAPI:
    """Test Invoice API endpoints"""
    
    async def test_create_invoice(
        self,
        client,
        auth_headers,
        invoice_factory
    ):
        """Test POST /api/v1/invoices"""
        data = invoice_factory()
        # Convert dates to ISO format
        data["issue_date"] = data["issue_date"].isoformat()
        data["due_date"] = data["due_date"].isoformat()
        
        response = await client.post(
            "/api/v1/invoices/",
            json=data,
            headers=auth_headers
        )
        
        assert response.status_code == 201
        result = response.json()
        assert result["invoice_number"] == data["invoice_number"]
        assert result["client_name"] == data["client_name"]
        assert result["amount"] == str(data["amount"])
        assert result["status"] == "pending"
        assert "id" in result
    
    async def test_create_invoice_duplicate_number(
        self,
        client,
        auth_headers,
        invoice_factory
    ):
        """Test that duplicate invoice numbers are rejected"""
        data = invoice_factory(invoice_number="INV-DUP-001")
        data["issue_date"] = data["issue_date"].isoformat()
        data["due_date"] = data["due_date"].isoformat()
        
        # Create first invoice
        await client.post(
            "/api/v1/invoices/",
            json=data,
            headers=auth_headers
        )
        
        # Try to create duplicate
        response = await client.post(
            "/api/v1/invoices/",
            json=data,
            headers=auth_headers
        )
        
        assert response.status_code == 400
        assert "already exists" in response.json()["detail"]
    
    async def test_list_invoices(
        self,
        client,
        auth_headers,
        invoice_factory
    ):
        """Test GET /api/v1/invoices"""
        # Create 3 invoices
        for i in range(3):
            data = invoice_factory(invoice_number=f"INV-{i}")
            data["issue_date"] = data["issue_date"].isoformat()
            data["due_date"] = data["due_date"].isoformat()
            await client.post(
                "/api/v1/invoices/",
                json=data,
                headers=auth_headers
            )
        
        # List invoices
        response = await client.get(
            "/api/v1/invoices/",
            headers=auth_headers
        )
        
        assert response.status_code == 200
        result = response.json()
        assert result["total"] == 3
        assert len(result["invoices"]) == 3
    
    async def test_list_invoices_with_filters(
        self,
        client,
        auth_headers,
        invoice_factory
    ):
        """Test filtering invoices"""
        # Create pending invoice
        pending_data = invoice_factory(invoice_number="INV-PENDING")
        pending_data["issue_date"] = pending_data["issue_date"].isoformat()
        pending_data["due_date"] = pending_data["due_date"].isoformat()
        await client.post(
            "/api/v1/invoices/",
            json=pending_data,
            headers=auth_headers
        )
        
        # Create paid invoice
        paid_data = invoice_factory(invoice_number="INV-PAID")
        paid_data["issue_date"] = paid_data["issue_date"].isoformat()
        paid_data["due_date"] = paid_data["due_date"].isoformat()
        paid_response = await client.post(
            "/api/v1/invoices/",
            json=paid_data,
            headers=auth_headers
        )
        paid_id = paid_response.json()["id"]
        
        # Mark as paid
        await client.patch(
            f"/api/v1/invoices/{paid_id}",
            json={"status": "paid"},
            headers=auth_headers
        )
        
        # Filter by status=pending
        response = await client.get(
            "/api/v1/invoices/?status=pending",
            headers=auth_headers
        )
        
        assert response.status_code == 200
        result = response.json()
        assert result["total"] == 1
        assert result["invoices"][0]["invoice_number"] == "INV-PENDING"
    
    async def test_list_invoices_pagination(
        self,
        client,
        auth_headers,
        invoice_factory
    ):
        """Test invoice pagination"""
        # Create 5 invoices
        for i in range(5):
            data = invoice_factory(invoice_number=f"INV-{i}")
            data["issue_date"] = data["issue_date"].isoformat()
            data["due_date"] = data["due_date"].isoformat()
            await client.post(
                "/api/v1/invoices/",
                json=data,
                headers=auth_headers
            )
        
        # Get page 1 with 2 items
        response = await client.get(
            "/api/v1/invoices/?page=1&page_size=2",
            headers=auth_headers
        )
        
        assert response.status_code == 200
        result = response.json()
        assert result["total"] == 5
        assert len(result["invoices"]) == 2
        assert result["total_pages"] == 3
    
    async def test_get_invoice(
        self,
        client,
        auth_headers,
        invoice_factory
    ):
        """Test GET /api/v1/invoices/{id}"""
        # Create invoice
        data = invoice_factory()
        data["issue_date"] = data["issue_date"].isoformat()
        data["due_date"] = data["due_date"].isoformat()
        create_response = await client.post(
            "/api/v1/invoices/",
            json=data,
            headers=auth_headers
        )
        invoice_id = create_response.json()["id"]
        
        # Get invoice
        response = await client.get(
            f"/api/v1/invoices/{invoice_id}",
            headers=auth_headers
        )
        
        assert response.status_code == 200
        result = response.json()
        assert result["id"] == invoice_id
    
    async def test_get_invoice_not_found(
        self,
        client,
        auth_headers
    ):
        """Test getting non-existent invoice"""
        response = await client.get(
            "/api/v1/invoices/00000000-0000-0000-0000-000000000000",
            headers=auth_headers
        )
        
        assert response.status_code == 404
    
    async def test_update_invoice(
        self,
        client,
        auth_headers,
        invoice_factory
    ):
        """Test PATCH /api/v1/invoices/{id}"""
        # Create invoice
        data = invoice_factory(amount=Decimal("1000.00"))
        data["issue_date"] = data["issue_date"].isoformat()
        data["due_date"] = data["due_date"].isoformat()
        create_response = await client.post(
            "/api/v1/invoices/",
            json=data,
            headers=auth_headers
        )
        invoice_id = create_response.json()["id"]
        
        # Update invoice
        response = await client.patch(
            f"/api/v1/invoices/{invoice_id}",
            json={"amount": 1500.00, "status": "paid"},
            headers=auth_headers
        )
        
        assert response.status_code == 200
        result = response.json()
        assert result["amount"] == "1500.00"
        assert result["status"] == "paid"
    
    async def test_delete_invoice(
        self,
        client,
        auth_headers,
        invoice_factory
    ):
        """Test DELETE /api/v1/invoices/{id}"""
        # Create invoice
        data = invoice_factory()
        data["issue_date"] = data["issue_date"].isoformat()
        data["due_date"] = data["due_date"].isoformat()
        create_response = await client.post(
            "/api/v1/invoices/",
            json=data,
            headers=auth_headers
        )
        invoice_id = create_response.json()["id"]
        
        # Delete invoice
        response = await client.delete(
            f"/api/v1/invoices/{invoice_id}",
            headers=auth_headers
        )
        
        assert response.status_code == 204
        
        # Verify deleted
        get_response = await client.get(
            f"/api/v1/invoices/{invoice_id}",
            headers=auth_headers
        )
        assert get_response.status_code == 404
    
    async def test_user_isolation(
        self,
        client,
        auth_headers,
        test_user_2,
        invoice_factory
    ):
        """Test that users cannot access each other's invoices"""
        from app.core.security import create_access_token
        
        # User 1 creates invoice
        data = invoice_factory()
        data["issue_date"] = data["issue_date"].isoformat()
        data["due_date"] = data["due_date"].isoformat()
        create_response = await client.post(
            "/api/v1/invoices/",
            json=data,
            headers=auth_headers
        )
        invoice_id = create_response.json()["id"]
        
        # User 2 tries to access
        user2_token = create_access_token(subject=str(test_user_2.id))
        user2_headers = {"Authorization": f"Bearer {user2_token}"}
        
        response = await client.get(
            f"/api/v1/invoices/{invoice_id}",
            headers=user2_headers
        )
        
        assert response.status_code == 404


