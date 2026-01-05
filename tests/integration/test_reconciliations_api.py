"""Integration tests for Reconciliation API"""
import pytest
from unittest.mock import AsyncMock, patch
from decimal import Decimal
from datetime import date, datetime, timedelta


@pytest.mark.asyncio
class TestReconciliationAPI:
    """Test Reconciliation API endpoints"""
    
    async def test_create_reconciliation_manual(
        self,
        client,
        auth_headers,
        db_session,
        test_user,
        invoice_factory,
        bank_account_factory,
        transaction_factory
    ):
        """Test manual reconciliation creation"""
        from app.schemas.invoice import InvoiceCreate
        from app.schemas.bank import BankAccountCreate
        from app.schemas.transaction import TransactionCreate
        from app.services.invoice_service import InvoiceService
        from app.services.bank_service import BankService
        from app.services.transaction_service import TransactionService
        
        # Create invoice
        invoice_data = InvoiceCreate(**invoice_factory(amount=Decimal("1000.00")))
        invoice = await InvoiceService.create_invoice(
            db_session,
            test_user.id,
            invoice_data
        )
        
        # Create bank account
        bank_data = BankAccountCreate(**bank_account_factory())
        bank_account = await BankService.create_bank_account(
            db_session,
            test_user.id,
            bank_data
        )
        
        # Create transaction
        tx_data = TransactionCreate(
            **transaction_factory(
                bank_account_id=bank_account.id,
                amount=Decimal("1000.00")
            )
        )
        transaction = await TransactionService.create_transaction(
            db_session,
            tx_data
        )
        
        await db_session.commit()
        
        # Create reconciliation
        response = await client.post(
            "/api/v1/reconciliations/",
            json={
                "transaction_id": str(transaction.id),
                "invoice_id": str(invoice.id),
                "match_score": 1.0,
                "match_method": "manual",
                "validated_by": "user"
            },
            headers=auth_headers
        )
        
        assert response.status_code == 201
        result = response.json()
        assert result["transaction_id"] == str(transaction.id)
        assert result["invoice_id"] == str(invoice.id)
        assert result["match_method"] == "manual"
    
    @patch('app.integrations.claude_client.ClaudeClient')
    async def test_get_reconciliation_suggestions(
        self,
        mock_claude,
        client,
        auth_headers,
        db_session,
        test_user,
        invoice_factory,
        bank_account_factory,
        transaction_factory
    ):
        """Test getting AI reconciliation suggestions"""
        # Mock Claude client
        mock_client_instance = AsyncMock()
        mock_client_instance.find_matching_invoice.return_value = {
            "invoice": {
                "invoice_number": "INV-TEST-001",
                "client_name": "Test Client",
                "total_amount": 1000.00,
                "currency": "EUR",
                "due_date": "2026-02-01"
            },
            "match_score": Decimal("0.95"),
            "match_method": "fuzzy_ai",
            "reasoning": "Montants correspondent exactement"
        }
        mock_claude.return_value = mock_client_instance
        
        # Setup data
        from app.schemas.invoice import InvoiceCreate
        from app.schemas.bank import BankAccountCreate
        from app.schemas.transaction import TransactionCreate
        from app.services.invoice_service import InvoiceService
        from app.services.bank_service import BankService
        from app.services.transaction_service import TransactionService
        
        # Create invoice
        invoice_data = InvoiceCreate(**invoice_factory(
            invoice_number="INV-TEST-001",
            amount=Decimal("1000.00")
        ))
        invoice = await InvoiceService.create_invoice(
            db_session,
            test_user.id,
            invoice_data
        )
        
        # Create bank account + transaction
        bank_data = BankAccountCreate(**bank_account_factory())
        bank_account = await BankService.create_bank_account(
            db_session,
            test_user.id,
            bank_data
        )
        
        tx_data = TransactionCreate(
            **transaction_factory(
                bank_account_id=bank_account.id,
                description="VIR CLIENT TEST",
                amount=Decimal("1000.00")
            )
        )
        transaction = await TransactionService.create_transaction(
            db_session,
            tx_data
        )
        
        await db_session.commit()
        
        # Get suggestions
        response = await client.get(
            f"/api/v1/reconciliations/suggestions/{transaction.id}",
            headers=auth_headers
        )
        
        assert response.status_code == 200
        suggestions = response.json()
        assert isinstance(suggestions, list)


