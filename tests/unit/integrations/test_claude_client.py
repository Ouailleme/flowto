"""Unit tests for Claude AI client (with mocks)"""
import pytest
from unittest.mock import AsyncMock, patch, MagicMock
from decimal import Decimal

from app.integrations.claude_client import ClaudeClient, ClaudeAIError


@pytest.mark.asyncio
class TestClaudeClient:
    """Test Claude AI client"""
    
    @patch('app.integrations.claude_client.anthropic.Anthropic')
    async def test_categorize_transaction_success(self, mock_anthropic):
        """Test successful transaction categorization"""
        # Mock Claude response
        mock_response = MagicMock()
        mock_response.content = [
            MagicMock(text='{"category": "loyer_bureau", "confidence": 0.95, "reasoning": "Description indique un loyer"}')
        ]
        
        mock_client = MagicMock()
        mock_client.messages.create.return_value = mock_response
        mock_anthropic.return_value = mock_client
        
        # Test
        client = ClaudeClient(api_key="test_key")
        category, confidence = await client.categorize_transaction(
            description="VIREMENT LOYER BUREAU JANVIER",
            amount=Decimal("1500.00"),
            transaction_type="debit"
        )
        
        assert category == "loyer_bureau"
        assert confidence == Decimal("0.95")
        assert mock_client.messages.create.called
    
    @patch('app.integrations.claude_client.anthropic.Anthropic')
    async def test_categorize_transaction_invalid_json(self, mock_anthropic):
        """Test handling of invalid JSON response"""
        # Mock invalid response
        mock_response = MagicMock()
        mock_response.content = [MagicMock(text='invalid json')]
        
        mock_client = MagicMock()
        mock_client.messages.create.return_value = mock_response
        mock_anthropic.return_value = mock_client
        
        # Test - should fallback to "autre" with 0.0 confidence
        client = ClaudeClient(api_key="test_key")
        category, confidence = await client.categorize_transaction(
            description="UNKNOWN TRANSACTION",
            amount=Decimal("100.00"),
            transaction_type="debit"
        )
        
        assert category == "autre"
        assert confidence == Decimal("0.0")
    
    @patch('app.integrations.claude_client.anthropic.Anthropic')
    async def test_find_matching_invoice_success(self, mock_anthropic):
        """Test successful invoice matching"""
        # Mock Claude response
        mock_response = MagicMock()
        mock_response.content = [
            MagicMock(text='{"match_found": true, "invoice_number": "INV-001", "match_score": 0.92, "match_method": "fuzzy_ai", "reasoning": "Montants correspondent"}')
        ]
        
        mock_client = MagicMock()
        mock_client.messages.create.return_value = mock_response
        mock_anthropic.return_value = mock_client
        
        # Test
        client = ClaudeClient(api_key="test_key")
        
        transaction = {
            "description": "VIR CLIENT ACME",
            "amount": 2500.00,
            "currency": "EUR",
            "date": "2026-01-05T10:00:00Z"
        }
        
        invoices = [
            {
                "invoice_number": "INV-001",
                "client_name": "ACME Corp",
                "total_amount": 2500.00,
                "currency": "EUR",
                "due_date": "2026-01-10"
            }
        ]
        
        result = await client.find_matching_invoice(transaction, invoices)
        
        assert result is not None
        assert result["invoice"]["invoice_number"] == "INV-001"
        assert result["match_score"] == Decimal("0.92")
        assert result["match_method"] == "fuzzy_ai"
    
    @patch('app.integrations.claude_client.anthropic.Anthropic')
    async def test_find_matching_invoice_no_match(self, mock_anthropic):
        """Test when no invoice matches"""
        # Mock Claude response
        mock_response = MagicMock()
        mock_response.content = [
            MagicMock(text='{"match_found": false, "invoice_number": null, "match_score": 0.0, "match_method": null, "reasoning": "Aucun match trouvé"}')
        ]
        
        mock_client = MagicMock()
        mock_client.messages.create.return_value = mock_response
        mock_anthropic.return_value = mock_client
        
        # Test
        client = ClaudeClient(api_key="test_key")
        
        transaction = {
            "description": "UNKNOWN",
            "amount": 999.00,
            "currency": "EUR",
            "date": "2026-01-05T10:00:00Z"
        }
        
        invoices = []
        
        result = await client.find_matching_invoice(transaction, invoices)
        
        assert result is None
    
    @patch('app.integrations.claude_client.anthropic.Anthropic')
    async def test_generate_reminder_email(self, mock_anthropic):
        """Test reminder email generation"""
        # Mock Claude response
        mock_response = MagicMock()
        mock_response.content = [
            MagicMock(text='{"subject": "Rappel: Facture INV-001", "body_html": "<html><p>Bonjour,</p><p>Rappel facture...</p></html>"}')
        ]
        
        mock_client = MagicMock()
        mock_client.messages.create.return_value = mock_response
        mock_anthropic.return_value = mock_client
        
        # Test
        client = ClaudeClient(api_key="test_key")
        
        invoice = {
            "invoice_number": "INV-001",
            "client_name": "ACME Corp",
            "total_amount": 2500.00,
            "currency": "EUR",
            "due_date": "2026-01-01",
            "days_overdue": 5
        }
        
        result = await client.generate_reminder_email(
            invoice=invoice,
            reminder_type="first",
            language="fr"
        )
        
        assert "subject" in result
        assert "body" in result
        assert "INV-001" in result["subject"]
        assert len(result["body"]) > 0


