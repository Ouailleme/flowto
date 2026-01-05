"""Reminder service - Automated invoice payment reminders"""
from typing import List
from sqlalchemy.ext.asyncio import AsyncSession
from uuid import UUID
from datetime import datetime, date, timedelta
import logging

from app.models.reminder import Reminder
from app.models.invoice import Invoice
from app.integrations.claude_client import ClaudeClient
from app.integrations.sendgrid_client import SendGridClient
from app.services.invoice_service import InvoiceService

logger = logging.getLogger(__name__)


class ReminderService:
    """Service for automated invoice payment reminders"""
    
    @staticmethod
    async def send_reminder(
        db: AsyncSession,
        invoice: Invoice,
        reminder_type: str,
        ai_client: ClaudeClient = None,
        email_client: SendGridClient = None
    ) -> Reminder:
        """
        Send a payment reminder for an invoice.
        
        Args:
            db: Database session
            invoice: Invoice to remind about
            reminder_type: first, second, final
            ai_client: Claude AI client
            email_client: SendGrid client
            
        Returns:
            Created reminder
        """
        if not invoice.client_email:
            raise ValueError("Invoice has no client email")
        
        # Initialize clients if not provided
        if ai_client is None:
            ai_client = ClaudeClient()
        if email_client is None:
            email_client = SendGridClient()
        
        # Generate email with AI
        invoice_data = {
            "invoice_number": invoice.invoice_number,
            "client_name": invoice.client_name,
            "total_amount": float(invoice.total_amount),
            "currency": invoice.currency,
            "due_date": invoice.due_date.isoformat(),
            "days_overdue": (date.today() - invoice.due_date).days
        }
        
        try:
            email_content = await ai_client.generate_reminder_email(
                invoice=invoice_data,
                reminder_type=reminder_type,
                language="fr"  # TODO: Use user's language preference
            )
            
            # Send email
            message_id = await email_client.send_reminder_email(
                invoice={"id": invoice.id, "invoice_number": invoice.invoice_number},
                client_email=invoice.client_email,
                client_name=invoice.client_name,
                subject=email_content["subject"],
                body_html=email_content["body"],
                reminder_type=reminder_type
            )
            
            # Create reminder record
            reminder = Reminder(
                invoice_id=invoice.id,
                reminder_type=reminder_type,
                email_subject=email_content["subject"],
                email_body=email_content["body"],
                sent_to=invoice.client_email,
                sent_at=datetime.utcnow(),
                status="sent",
                email_provider_id=message_id
            )
            
            db.add(reminder)
            await db.flush()
            
            logger.info(
                f"Reminder sent for invoice {invoice.invoice_number} "
                f"({reminder_type}) to {invoice.client_email}"
            )
            
            return reminder
            
        except Exception as e:
            logger.error(f"Failed to send reminder for invoice {invoice.id}: {e}")
            raise
    
    @staticmethod
    async def process_overdue_invoices(
        db: AsyncSession,
        user_id: UUID = None,
        ai_client: ClaudeClient = None,
        email_client: SendGridClient = None
    ) -> dict:
        """
        Process all overdue invoices and send appropriate reminders.
        
        Logic:
        - 1-7 days overdue: First reminder
        - 8-14 days overdue: Second reminder
        - 15+ days overdue: Final reminder
        
        Args:
            db: Database session
            user_id: User ID (optional, process all users if None)
            ai_client: Claude AI client
            email_client: SendGrid client
            
        Returns:
            Stats dict with counts
        """
        # Get overdue invoices
        overdue_invoices = await InvoiceService.get_overdue_invoices(
            db,
            user_id
        )
        
        if not overdue_invoices:
            return {"total": 0, "sent": 0, "failed": 0}
        
        stats = {"total": len(overdue_invoices), "sent": 0, "failed": 0}
        
        for invoice in overdue_invoices:
            try:
                days_overdue = (date.today() - invoice.due_date).days
                
                # Determine reminder type
                if days_overdue >= 15:
                    reminder_type = "final"
                elif days_overdue >= 8:
                    reminder_type = "second"
                else:
                    reminder_type = "first"
                
                # Check if reminder already sent
                from sqlalchemy import select, and_
                existing = await db.execute(
                    select(Reminder)
                    .where(
                        and_(
                            Reminder.invoice_id == invoice.id,
                            Reminder.reminder_type == reminder_type,
                            Reminder.sent_at >= datetime.utcnow() - timedelta(days=3)
                        )
                    )
                )
                
                if existing.scalar_one_or_none():
                    logger.info(
                        f"Reminder already sent recently for invoice {invoice.invoice_number}"
                    )
                    continue
                
                # Send reminder
                await ReminderService.send_reminder(
                    db,
                    invoice,
                    reminder_type,
                    ai_client,
                    email_client
                )
                
                stats["sent"] += 1
                
            except Exception as e:
                logger.error(f"Failed to process invoice {invoice.id}: {e}")
                stats["failed"] += 1
        
        await db.commit()
        
        logger.info(
            f"Processed {stats['total']} overdue invoices: "
            f"{stats['sent']} sent, {stats['failed']} failed"
        )
        
        return stats
    
    @staticmethod
    async def get_reminder_stats(
        db: AsyncSession,
        user_id: UUID
    ) -> dict:
        """
        Get reminder statistics for user.
        
        Returns:
            Stats dict
        """
        from sqlalchemy import select, func, and_
        
        # Total reminders
        total_result = await db.execute(
            select(func.count(Reminder.id))
            .join(Invoice)
            .where(Invoice.user_id == user_id)
        )
        total = total_result.scalar() or 0
        
        # By type
        type_result = await db.execute(
            select(
                Reminder.reminder_type,
                func.count(Reminder.id)
            )
            .join(Invoice)
            .where(Invoice.user_id == user_id)
            .group_by(Reminder.reminder_type)
        )
        by_type = dict(type_result.all())
        
        # Open rate
        opened_result = await db.execute(
            select(func.count(Reminder.id))
            .join(Invoice)
            .where(
                and_(
                    Invoice.user_id == user_id,
                    Reminder.opened_at.is_not(None)
                )
            )
        )
        opened = opened_result.scalar() or 0
        
        open_rate = (opened / total * 100) if total > 0 else 0
        
        return {
            "total": total,
            "by_type": by_type,
            "opened": opened,
            "open_rate": round(open_rate, 2)
        }


