"""SendGrid client for email sending"""
from typing import List, Dict, Optional
import httpx
import logging
import base64

from app.config import settings

logger = logging.getLogger(__name__)


class SendGridError(Exception):
    """SendGrid error"""
    pass


class SendGridClient:
    """
    Client for SendGrid (email delivery)
    
    Doc: https://docs.sendgrid.com/api-reference
    """
    
    BASE_URL = "https://api.sendgrid.com/v3"
    
    def __init__(self, api_key: str = None):
        """Initialize SendGrid client"""
        self.api_key = api_key or settings.SENDGRID_API_KEY
        
        self.client = httpx.AsyncClient(
            timeout=30.0,
            headers={
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json"
            }
        )
    
    async def close(self):
        """Close HTTP client"""
        await self.client.aclose()
    
    async def send_email(
        self,
        to_email: str,
        to_name: str,
        subject: str,
        html_content: str,
        from_email: str = "noreply@financeai.com",
        from_name: str = "FinanceAI",
        reply_to: Optional[str] = None,
        custom_args: Optional[Dict] = None
    ) -> str:
        """
        Send an email via SendGrid.
        
        Args:
            to_email: Recipient email
            to_name: Recipient name
            subject: Email subject
            html_content: Email body (HTML)
            from_email: Sender email
            from_name: Sender name
            reply_to: Reply-to email
            custom_args: Custom tracking arguments
            
        Returns:
            SendGrid message ID
        """
        payload = {
            "personalizations": [
                {
                    "to": [{"email": to_email, "name": to_name}],
                    "subject": subject,
                }
            ],
            "from": {"email": from_email, "name": from_name},
            "content": [
                {
                    "type": "text/html",
                    "value": html_content
                }
            ],
            "tracking_settings": {
                "click_tracking": {"enable": True},
                "open_tracking": {"enable": True}
            }
        }
        
        if reply_to:
            payload["reply_to"] = {"email": reply_to}
        
        if custom_args:
            payload["custom_args"] = custom_args
        
        try:
            response = await self.client.post(
                f"{self.BASE_URL}/mail/send",
                json=payload
            )
            response.raise_for_status()
            
            # SendGrid returns message ID in X-Message-Id header
            message_id = response.headers.get("X-Message-Id", "unknown")
            
            logger.info(
                f"Email sent to {to_email}: '{subject}' "
                f"(message_id: {message_id})"
            )
            
            return message_id
            
        except httpx.HTTPStatusError as e:
            logger.error(f"SendGrid send email failed: {e.response.text}")
            raise SendGridError(f"Failed to send email: {e}")
        except httpx.RequestError as e:
            logger.error(f"SendGrid request error: {e}")
            raise SendGridError(f"SendGrid request error: {e}")
    
    async def send_reminder_email(
        self,
        invoice: Dict,
        client_email: str,
        client_name: str,
        subject: str,
        body_html: str,
        reminder_type: str
    ) -> str:
        """
        Send invoice reminder email.
        
        Args:
            invoice: Invoice data
            client_email: Client email
            client_name: Client name
            subject: Email subject
            body_html: Email body HTML
            reminder_type: first, second, final
            
        Returns:
            SendGrid message ID
        """
        custom_args = {
            "invoice_id": str(invoice["id"]),
            "invoice_number": invoice["invoice_number"],
            "reminder_type": reminder_type
        }
        
        message_id = await self.send_email(
            to_email=client_email,
            to_name=client_name,
            subject=subject,
            html_content=body_html,
            custom_args=custom_args
        )
        
        return message_id
    
    async def get_email_stats(self, message_id: str) -> Dict:
        """
        Get email delivery stats (opens, clicks, bounces).
        
        Args:
            message_id: SendGrid message ID
            
        Returns:
            Email stats
        """
        try:
            response = await self.client.get(
                f"{self.BASE_URL}/messages/{message_id}"
            )
            response.raise_for_status()
            
            data = response.json()
            
            return {
                "status": data.get("status"),
                "opens": data.get("opens_count", 0),
                "clicks": data.get("clicks_count", 0),
                "last_event_time": data.get("last_event_time")
            }
            
        except httpx.HTTPStatusError as e:
            logger.error(f"SendGrid get stats failed: {e.response.text}")
            return {"status": "unknown", "opens": 0, "clicks": 0}
        except httpx.RequestError as e:
            logger.error(f"SendGrid request error: {e}")
            return {"status": "unknown", "opens": 0, "clicks": 0}
    
    async def send_bulk_emails(
        self,
        emails: List[Dict]
    ) -> List[str]:
        """
        Send multiple emails (batch).
        
        Args:
            emails: List of email dicts with to_email, subject, html_content
            
        Returns:
            List of message IDs
        """
        message_ids = []
        
        for email in emails:
            try:
                message_id = await self.send_email(
                    to_email=email["to_email"],
                    to_name=email.get("to_name", ""),
                    subject=email["subject"],
                    html_content=email["html_content"],
                    custom_args=email.get("custom_args")
                )
                message_ids.append(message_id)
            except SendGridError as e:
                logger.error(f"Failed to send email to {email['to_email']}: {e}")
                message_ids.append(None)
        
        return message_ids
    
    async def send_email_with_attachment(
        self,
        to_email: str,
        subject: str,
        content: str,
        attachment_content: bytes,
        attachment_filename: str,
        attachment_type: str = "application/pdf",
        from_email: str = "noreply@flowto.fr",
        from_name: str = "Flowto"
    ) -> str:
        """
        Send an email with file attachment.
        
        Args:
            to_email: Recipient email
            subject: Email subject
            content: Email body (plain text)
            attachment_content: File content as bytes
            attachment_filename: Filename for attachment
            attachment_type: MIME type of attachment
            from_email: Sender email
            from_name: Sender name
            
        Returns:
            SendGrid message ID
        """
        # Encode attachment to base64
        encoded_attachment = base64.b64encode(attachment_content).decode()
        
        payload = {
            "personalizations": [
                {
                    "to": [{"email": to_email}],
                    "subject": subject,
                }
            ],
            "from": {"email": from_email, "name": from_name},
            "content": [
                {
                    "type": "text/plain",
                    "value": content
                }
            ],
            "attachments": [
                {
                    "content": encoded_attachment,
                    "filename": attachment_filename,
                    "type": attachment_type,
                    "disposition": "attachment"
                }
            ]
        }
        
        try:
            response = await self.client.post(
                f"{self.BASE_URL}/mail/send",
                json=payload
            )
            response.raise_for_status()
            
            message_id = response.headers.get("X-Message-Id", "unknown")
            
            logger.info(
                f"Email with attachment sent to {to_email}: '{subject}' "
                f"(message_id: {message_id}, attachment: {attachment_filename})"
            )
            
            return message_id
            
        except httpx.HTTPStatusError as e:
            logger.error(f"SendGrid send email with attachment failed: {e.response.text}")
            raise SendGridError(f"Failed to send email with attachment: {e}")
        except httpx.RequestError as e:
            logger.error(f"SendGrid request error: {e}")
            raise SendGridError(f"SendGrid request error: {e}")


