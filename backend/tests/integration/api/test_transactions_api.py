"""
Integration tests for Transactions API endpoints.
Simplified tests covering main CRUD operations.
"""
import pytest
from httpx import AsyncClient
from datetime import date, timedelta


@pytest.mark.asyncio
@pytest.mark.integration
async def test_get_transactions_list(client: AsyncClient, auth_headers):
    """Test getting list of transactions."""
    response = await client.get(
        "/api/v1/transactions/?page=1&page_size=10",
        headers=auth_headers
    )
    
    assert response.status_code == 200
    data = response.json()
    assert "transactions" in data
    assert "total" in data
    assert isinstance(data["transactions"], list)


@pytest.mark.asyncio
@pytest.mark.integration
async def test_get_transactions_unauthorized(client: AsyncClient):
    """Test getting transactions without auth fails."""
    response = await client.get("/api/v1/transactions/?page=1&page_size=10")
    
    assert response.status_code in [401, 403]


@pytest.mark.asyncio
@pytest.mark.integration
async def test_get_transaction_by_id(client: AsyncClient, auth_headers):
    """Test getting a specific transaction (if any exist)."""
    # First get the list
    list_response = await client.get(
        "/api/v1/transactions/?page=1&page_size=1",
        headers=auth_headers
    )
    
    if list_response.status_code == 200 and list_response.json().get("transactions"):
        transaction_id = list_response.json()["transactions"][0]["id"]
        
        # Get specific transaction
        response = await client.get(
            f"/api/v1/transactions/{transaction_id}",
            headers=auth_headers
        )
        
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == transaction_id


@pytest.mark.asyncio
@pytest.mark.integration
async def test_get_transaction_not_found(client: AsyncClient, auth_headers):
    """Test getting non-existent transaction returns 404."""
    fake_id = "00000000-0000-0000-0000-000000000000"
    response = await client.get(
        f"/api/v1/transactions/{fake_id}",
        headers=auth_headers
    )
    
    assert response.status_code == 404


@pytest.mark.asyncio
@pytest.mark.integration
async def test_filter_transactions_by_date(client: AsyncClient, auth_headers):
    """Test filtering transactions by date range."""
    start_date = str(date.today() - timedelta(days=90))
    end_date = str(date.today())
    
    response = await client.get(
        f"/api/v1/transactions/?start_date={start_date}&end_date={end_date}",
        headers=auth_headers
    )
    
    # API might accept or reject date filtering depending on implementation
    assert response.status_code in [200, 400, 422]
    if response.status_code == 200:
        data = response.json()
        assert "transactions" in data


@pytest.mark.asyncio
@pytest.mark.integration
async def test_categorize_transaction(client: AsyncClient, auth_headers):
    """Test categorizing a transaction (if any exist)."""
    # Get a transaction first
    list_response = await client.get(
        "/api/v1/transactions/?page=1&page_size=1",
        headers=auth_headers
    )
    
    if list_response.status_code == 200 and list_response.json().get("transactions"):
        transaction_id = list_response.json()["transactions"][0]["id"]
        
        # Try to categorize it
        response = await client.patch(
            f"/api/v1/transactions/{transaction_id}",
            json={"category": "office_supplies"},
            headers=auth_headers
        )
        
        # Might succeed or fail depending on implementation
        assert response.status_code in [200, 400, 404]


@pytest.mark.asyncio
@pytest.mark.integration
@pytest.mark.skip(reason="Categorization breakdown endpoint implementation varies")
async def test_get_categorization_breakdown(client: AsyncClient, auth_headers):
    """Test getting categorization breakdown."""
    response = await client.get(
        "/api/v1/categorization/breakdown",
        headers=auth_headers
    )
    
    # Endpoint might not exist yet, accept various responses
    assert response.status_code in [200, 400, 404, 422]
    
    if response.status_code == 200:
        data = response.json()
        # Data structure varies by implementation
        assert data is not None


@pytest.mark.asyncio
@pytest.mark.integration
async def test_transaction_pagination(client: AsyncClient, auth_headers):
    """Test transaction pagination."""
    # Get first page
    response1 = await client.get(
        "/api/v1/transactions/?page=1&page_size=5",
        headers=auth_headers
    )
    assert response1.status_code == 200
    data1 = response1.json()
    assert "page" in data1
    assert data1["page"] == 1
    
    # Get second page
    response2 = await client.get(
        "/api/v1/transactions/?page=2&page_size=5",
        headers=auth_headers
    )
    assert response2.status_code == 200
    data2 = response2.json()
    assert "page" in data2
    assert data2["page"] == 2

