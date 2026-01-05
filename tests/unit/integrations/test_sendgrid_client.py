"""Unit tests for SendGrid client (with mocks)"""
import pytest
from unittest.mock import AsyncMock, patch, MagicMock
import httpx

from app.integrations.sendgrid_client import SendGridClient, SendGridError


@pytest.mark.asyncio
class TestSendGridClient:
    """Test SendGrid client"""
    
    @patch('httpx.AsyncClient')
    async def test_send_email_success(self, mock_async_client):
        """Test successful email sending"""
        # Mock response
        mock_response = MagicMock()
        mock_response.status_code = 202
        mock_response.headers = {"X-Message-Id": "test-message-id-123"}
        mock_response.raise_for_status = MagicMock()
        
        mock_client_instance = AsyncMock()
        mock_client_instance.post.return_value = mock_response
        mock_async_client.return_value = mock_client_instance
        
        # Test
        client = SendGridClient(api_key="test_key")
        
        message_id = await client.send_email(
            to_email="test@example.com",
            to_name="Test User",
            subject="Test Email",
            html_content="<p>Test content</p>"
        )
        
        assert message_id == "test-message-id-123"
        assert mock_client_instance.post.called
    
    @patch('httpx.AsyncClient')
    async def test_send_email_failure(self, mock_async_client):
        """Test email sending failure"""
        # Mock error response
        mock_response = MagicMock()
        mock_response.status_code = 400
        mock_response.text = "Bad request"
        mock_response.raise_for_status.side_effect = httpx.HTTPStatusError(
            "400 Bad Request",
            request=MagicMock(),
            response=mock_response
        )
        
        mock_client_instance = AsyncMock()
        mock_client_instance.post.return_value = mock_response
        mock_async_client.return_value = mock_client_instance
        
        # Test
        client = SendGridClient(api_key="test_key")
        
        with pytest.raises(SendGridError):
            await client.send_email(
                to_email="invalid@example.com",
                to_name="Test User",
                subject="Test Email",
                html_content="<p>Test content</p>"
            )
    
    @patch('httpx.AsyncClient')
    async def test_send_reminder_email(self, mock_async_client):
        """Test sending reminder email"""
        # Mock response
        mock_response = MagicMock()
        mock_response.status_code = 202
        mock_response.headers = {"X-Message-Id": "reminder-msg-123"}
        mock_response.raise_for_status = MagicMock()
        
        mock_client_instance = AsyncMock()
        mock_client_instance.post.return_value = mock_response
        mock_async_client.return_value = mock_client_instance
        
        # Test
        client = SendGridClient(api_key="test_key")
        
        invoice = {
            "id": "invoice-123",
            "invoice_number": "INV-001"
        }
        
        message_id = await client.send_reminder_email(
            invoice=invoice,
            client_email="client@example.com",
            client_name="ACME Corp",
            subject="Rappel: Facture INV-001",
            body_html="<p>Rappel de paiement</p>",
            reminder_type="first"
        )
        
        assert message_id == "reminder-msg-123"
        
        # Verify custom args were passed
        call_args = mock_client_instance.post.call_args
        json_data = call_args[1]["json"]
        assert "custom_args" in json_data
        assert json_data["custom_args"]["invoice_number"] == "INV-001"


