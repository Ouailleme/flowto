"""Integration tests for Bank API endpoints"""
import pytest
from decimal import Decimal


@pytest.mark.asyncio
class TestBankAPI:
    """Test Bank API endpoints"""
    
    async def test_create_bank_account(
        self,
        client,
        auth_headers,
        bank_account_factory
    ):
        """Test POST /api/v1/banks"""
        data = bank_account_factory()
        
        response = await client.post(
            "/api/v1/banks/",
            json=data,
            headers=auth_headers
        )
        
        assert response.status_code == 201
        result = response.json()
        assert result["bank_name"] == data["bank_name"]
        assert result["balance"] == str(data["balance"])
        assert "id" in result
    
    async def test_create_bank_account_unauthorized(
        self,
        client,
        bank_account_factory
    ):
        """Test that creating bank account requires auth"""
        data = bank_account_factory()
        
        response = await client.post(
            "/api/v1/banks/",
            json=data
        )
        
        assert response.status_code == 401
    
    async def test_list_bank_accounts(
        self,
        client,
        auth_headers,
        bank_account_factory
    ):
        """Test GET /api/v1/banks"""
        # Create 2 accounts
        for i in range(2):
            await client.post(
                "/api/v1/banks/",
                json=bank_account_factory(bank_name=f"Bank {i}"),
                headers=auth_headers
            )
        
        # List accounts
        response = await client.get(
            "/api/v1/banks/",
            headers=auth_headers
        )
        
        assert response.status_code == 200
        result = response.json()
        assert result["total"] == 2
        assert len(result["accounts"]) == 2
    
    async def test_get_bank_account(
        self,
        client,
        auth_headers,
        bank_account_factory
    ):
        """Test GET /api/v1/banks/{id}"""
        # Create account
        create_response = await client.post(
            "/api/v1/banks/",
            json=bank_account_factory(),
            headers=auth_headers
        )
        account_id = create_response.json()["id"]
        
        # Get account
        response = await client.get(
            f"/api/v1/banks/{account_id}",
            headers=auth_headers
        )
        
        assert response.status_code == 200
        result = response.json()
        assert result["id"] == account_id
    
    async def test_get_bank_account_not_found(
        self,
        client,
        auth_headers
    ):
        """Test getting non-existent bank account"""
        response = await client.get(
            "/api/v1/banks/00000000-0000-0000-0000-000000000000",
            headers=auth_headers
        )
        
        assert response.status_code == 404
    
    async def test_update_bank_account(
        self,
        client,
        auth_headers,
        bank_account_factory
    ):
        """Test PATCH /api/v1/banks/{id}"""
        # Create account
        create_response = await client.post(
            "/api/v1/banks/",
            json=bank_account_factory(balance=Decimal("1000.00")),
            headers=auth_headers
        )
        account_id = create_response.json()["id"]
        
        # Update account
        response = await client.patch(
            f"/api/v1/banks/{account_id}",
            json={"balance": 2000.00, "is_active": False},
            headers=auth_headers
        )
        
        assert response.status_code == 200
        result = response.json()
        assert result["balance"] == "2000.00"
        assert result["is_active"] is False
    
    async def test_delete_bank_account(
        self,
        client,
        auth_headers,
        bank_account_factory
    ):
        """Test DELETE /api/v1/banks/{id}"""
        # Create account
        create_response = await client.post(
            "/api/v1/banks/",
            json=bank_account_factory(),
            headers=auth_headers
        )
        account_id = create_response.json()["id"]
        
        # Delete account
        response = await client.delete(
            f"/api/v1/banks/{account_id}",
            headers=auth_headers
        )
        
        assert response.status_code == 204
        
        # Verify deleted
        get_response = await client.get(
            f"/api/v1/banks/{account_id}",
            headers=auth_headers
        )
        assert get_response.status_code == 404
    
    async def test_user_isolation(
        self,
        client,
        auth_headers,
        test_user_2,
        bank_account_factory
    ):
        """Test that users cannot access each other's bank accounts"""
        from app.core.security import create_access_token
        
        # User 1 creates account
        create_response = await client.post(
            "/api/v1/banks/",
            json=bank_account_factory(),
            headers=auth_headers
        )
        account_id = create_response.json()["id"]
        
        # User 2 tries to access
        user2_token = create_access_token(subject=str(test_user_2.id))
        user2_headers = {"Authorization": f"Bearer {user2_token}"}
        
        response = await client.get(
            f"/api/v1/banks/{account_id}",
            headers=user2_headers
        )
        
        assert response.status_code == 404


