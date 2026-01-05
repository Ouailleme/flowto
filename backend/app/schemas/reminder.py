"""Reminder Pydantic schemas"""
from pydantic import BaseModel, Field, ConfigDict
from uuid import UUID
from datetime import datetime
from typing import Optional


class ReminderCreate(BaseModel):
    """Schema for creating a reminder"""
    invoice_id: UUID
    reminder_type: str = Field(..., pattern="^(first|second|final)$")
    email_subject: str = Field(..., min_length=1, max_length=255)
    email_body: str = Field(..., min_length=1)
    sent_to: str = Field(..., min_length=1, max_length=255)
    
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "invoice_id": "123e4567-e89b-12d3-a456-426614174000",
                "reminder_type": "first",
                "email_subject": "Rappel: Facture INV-2026-001",
                "email_body": "<html>...</html>",
                "sent_to": "client@example.com"
            }
        }
    )


class ReminderRead(BaseModel):
    """Schema for reading reminder (response)"""
    model_config = ConfigDict(from_attributes=True)
    
    id: UUID
    invoice_id: UUID
    reminder_type: str
    email_subject: str
    sent_to: str
    sent_at: datetime
    opened_at: Optional[datetime]
    clicked_at: Optional[datetime]
    status: str
    created_at: datetime


class ReminderList(BaseModel):
    """Schema for list of reminders"""
    reminders: list[ReminderRead]
    total: int


