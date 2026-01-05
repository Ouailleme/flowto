"""Reconciliation Pydantic schemas"""
from pydantic import BaseModel, Field, ConfigDict
from uuid import UUID
from datetime import datetime
from decimal import Decimal
from typing import Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from app.schemas.transaction import TransactionRead
    from app.schemas.invoice import InvoiceRead


class ReconciliationCreate(BaseModel):
    """Schema for creating a reconciliation"""
    transaction_id: UUID
    invoice_id: UUID
    match_score: Decimal = Field(..., ge=0, le=1)
    match_method: str = Field(..., pattern="^(exact|reference|fuzzy_ai|manual)$")
    ai_reasoning: Optional[str] = Field(None, max_length=1000)
    validated_by: str = Field(..., pattern="^(ai|user)$")
    notes: Optional[str] = Field(None, max_length=500)
    
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "transaction_id": "123e4567-e89b-12d3-a456-426614174000",
                "invoice_id": "123e4567-e89b-12d3-a456-426614174001",
                "match_score": 0.95,
                "match_method": "exact",
                "validated_by": "ai"
            }
        }
    )


class ReconciliationUpdate(BaseModel):
    """Schema for updating reconciliation"""
    validated_by: Optional[str] = Field(None, pattern="^(ai|user)$")
    notes: Optional[str] = Field(None, max_length=500)


class ReconciliationRead(BaseModel):
    """Schema for reading reconciliation (response)"""
    model_config = ConfigDict(from_attributes=True)
    
    id: UUID
    user_id: UUID
    transaction_id: UUID
    invoice_id: UUID
    match_score: Decimal
    match_method: str
    ai_reasoning: Optional[str]
    validated_by: str
    validated_at: datetime
    notes: Optional[str]
    created_at: datetime


class ReconciliationWithDetails(ReconciliationRead):
    """Schema for reconciliation with transaction and invoice details"""
    transaction: "TransactionRead"
    invoice: "InvoiceRead"


class ReconciliationSuggestion(BaseModel):
    """Schema for AI reconciliation suggestion"""
    transaction_id: UUID
    invoice_id: UUID
    match_score: Decimal
    match_method: str
    reasoning: str
    transaction_description: str
    transaction_amount: Decimal
    invoice_number: str
    invoice_amount: Decimal
    
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "transaction_id": "123e4567-e89b-12d3-a456-426614174000",
                "invoice_id": "123e4567-e89b-12d3-a456-426614174001",
                "match_score": 0.92,
                "match_method": "fuzzy_ai",
                "reasoning": "Amounts match exactly (2500.00 EUR), dates are 2 days apart, client name found in transaction description",
                "transaction_description": "VIR ACME CORP INVOICE 001",
                "transaction_amount": 2500.00,
                "invoice_number": "INV-2026-001",
                "invoice_amount": 2500.00
            }
        }
    )


class ReconciliationList(BaseModel):
    """Schema for list of reconciliations"""
    reconciliations: list[ReconciliationRead]
    total: int

