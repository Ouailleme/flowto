"""Integration tests for Categorization API"""
import pytest
from unittest.mock import AsyncMock, patch
from decimal import Decimal


@pytest.mark.asyncio
class TestCategorizationAPI:
    """Test Categorization API endpoints"""
    
    @patch('app.integrations.claude_client.ClaudeClient')
    async def test_categorize_single_transaction(
        self,
        mock_claude,
        client,
        auth_headers,
        db_session,
        test_user,
        bank_account_factory,
        transaction_factory
    ):
        """Test categorizing a single transaction"""
        # Mock Claude
        mock_client_instance = AsyncMock()
        mock_client_instance.categorize_transaction.return_value = (
            "loyer_bureau",
            Decimal("0.95")
        )
        mock_claude.return_value = mock_client_instance
        
        # Setup data
        from app.schemas.bank import BankAccountCreate
        from app.schemas.transaction import TransactionCreate
        from app.services.bank_service import BankService
        from app.services.transaction_service import TransactionService
        
        bank_data = BankAccountCreate(**bank_account_factory())
        bank_account = await BankService.create_bank_account(
            db_session,
            test_user.id,
            bank_data
        )
        
        tx_data = TransactionCreate(
            **transaction_factory(
                bank_account_id=bank_account.id,
                description="VIREMENT LOYER JANVIER"
            )
        )
        transaction = await TransactionService.create_transaction(
            db_session,
            tx_data
        )
        
        await db_session.commit()
        
        # Categorize
        response = await client.post(
            f"/api/v1/categorization/transactions/{transaction.id}",
            headers=auth_headers
        )
        
        assert response.status_code == 200
        result = response.json()
        assert result["category"] == "loyer_bureau"
        assert float(result["category_confidence"]) == 0.95
    
    @patch('app.integrations.claude_client.ClaudeClient')
    async def test_categorize_bulk(
        self,
        mock_claude,
        client,
        auth_headers,
        db_session,
        test_user,
        bank_account_factory,
        transaction_factory
    ):
        """Test bulk categorization"""
        # Mock Claude
        mock_client_instance = AsyncMock()
        mock_client_instance.categorize_transaction.return_value = (
            "fournitures_bureau",
            Decimal("0.85")
        )
        mock_claude.return_value = mock_client_instance
        
        # Setup data
        from app.schemas.bank import BankAccountCreate
        from app.schemas.transaction import TransactionCreate
        from app.services.bank_service import BankService
        from app.services.transaction_service import TransactionService
        
        bank_data = BankAccountCreate(**bank_account_factory())
        bank_account = await BankService.create_bank_account(
            db_session,
            test_user.id,
            bank_data
        )
        
        # Create 3 uncategorized transactions
        for i in range(3):
            tx_data = TransactionCreate(
                **transaction_factory(
                    bank_account_id=bank_account.id,
                    description=f"TRANSACTION {i}"
                )
            )
            await TransactionService.create_transaction(db_session, tx_data)
        
        await db_session.commit()
        
        # Bulk categorize
        response = await client.post(
            "/api/v1/categorization/bulk?limit=10",
            headers=auth_headers
        )
        
        assert response.status_code == 200
        result = response.json()
        assert result["categorized"] >= 3
    
    async def test_get_category_breakdown(
        self,
        client,
        auth_headers,
        db_session,
        test_user,
        bank_account_factory,
        transaction_factory
    ):
        """Test getting category breakdown"""
        # Setup data
        from app.schemas.bank import BankAccountCreate
        from app.schemas.transaction import TransactionCreate
        from app.services.bank_service import BankService
        from app.services.transaction_service import TransactionService
        
        bank_data = BankAccountCreate(**bank_account_factory())
        bank_account = await BankService.create_bank_account(
            db_session,
            test_user.id,
            bank_data
        )
        
        # Create transactions with categories
        categories = [
            ("loyer_bureau", Decimal("-1500.00")),
            ("loyer_bureau", Decimal("-1500.00")),
            ("fournitures_bureau", Decimal("-200.00"))
        ]
        
        for category, amount in categories:
            tx_data = TransactionCreate(
                **transaction_factory(
                    bank_account_id=bank_account.id,
                    amount=amount
                )
            )
            tx = await TransactionService.create_transaction(db_session, tx_data)
            tx.category = category
            tx.category_confidence = Decimal("0.95")
        
        await db_session.commit()
        
        # Get breakdown
        response = await client.get(
            "/api/v1/categorization/breakdown",
            headers=auth_headers
        )
        
        assert response.status_code == 200
        breakdown = response.json()
        assert isinstance(breakdown, dict)
        assert "loyer_bureau" in breakdown
        assert "fournitures_bureau" in breakdown


