"""Transaction Pydantic schemas"""
from pydantic import BaseModel, Field, ConfigDict
from uuid import UUID
from datetime import datetime
from decimal import Decimal
from typing import Optional


class TransactionCreate(BaseModel):
    """Schema for creating a transaction (usually from sync)"""
    bank_account_id: UUID
    date: datetime
    description: str = Field(..., min_length=1, max_length=500)
    amount: Decimal
    currency: str = Field(default="EUR", min_length=3, max_length=3)
    transaction_type: Optional[str] = Field(None, max_length=50)
    bridge_transaction_id: Optional[str] = None
    external_id: Optional[str] = None
    
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "bank_account_id": "123e4567-e89b-12d3-a456-426614174000",
                "date": "2026-01-05T14:30:00Z",
                "description": "VIR LOYER BUREAU JANVIER",
                "amount": -1500.00,
                "currency": "EUR",
                "transaction_type": "debit"
            }
        }
    )


class TransactionUpdate(BaseModel):
    """Schema for updating transaction (mainly category)"""
    category: Optional[str] = Field(None, max_length=100)
    category_confidence: Optional[Decimal] = Field(None, ge=0, le=1)
    description: Optional[str] = Field(None, min_length=1, max_length=500)


class TransactionRead(BaseModel):
    """Schema for reading transaction (response)"""
    model_config = ConfigDict(from_attributes=True)
    
    id: UUID
    bank_account_id: UUID
    date: datetime
    description: str
    amount: Decimal
    currency: str
    amount_converted: Optional[Decimal]
    conversion_rate: Optional[Decimal]
    transaction_type: Optional[str]
    category: Optional[str]
    category_confidence: Optional[Decimal]
    is_reconciled: bool
    reconciliation_id: Optional[UUID]
    created_at: datetime


class TransactionFilter(BaseModel):
    """Schema for filtering transactions"""
    bank_account_id: Optional[UUID] = None
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    category: Optional[str] = None
    is_reconciled: Optional[bool] = None
    min_amount: Optional[Decimal] = None
    max_amount: Optional[Decimal] = None
    search: Optional[str] = Field(None, max_length=255)


class TransactionList(BaseModel):
    """Schema for list of transactions with pagination"""
    transactions: list[TransactionRead]
    total: int
    page: int
    page_size: int
    total_pages: int


