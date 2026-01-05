"""Bank Account Pydantic schemas"""
from pydantic import BaseModel, Field, ConfigDict
from uuid import UUID
from datetime import datetime
from decimal import Decimal
from typing import Optional


class BankAccountCreate(BaseModel):
    """Schema for creating a bank account (manual entry)"""
    bank_name: str = Field(..., min_length=1, max_length=255)
    account_type: Optional[str] = Field(None, max_length=50)
    iban: Optional[str] = Field(None, max_length=100)
    balance: Decimal = Field(default=Decimal("0.00"), ge=0)
    currency: str = Field(default="EUR", min_length=3, max_length=3)
    
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "bank_name": "BNP Paribas",
                "account_type": "checking",
                "iban": "FR7630006000011234567890189",
                "balance": 5000.00,
                "currency": "EUR"
            }
        }
    )


class BankAccountUpdate(BaseModel):
    """Schema for updating bank account"""
    bank_name: Optional[str] = Field(None, min_length=1, max_length=255)
    account_type: Optional[str] = Field(None, max_length=50)
    balance: Optional[Decimal] = Field(None, ge=0)
    is_active: Optional[bool] = None


class BankAccountRead(BaseModel):
    """Schema for reading bank account (response)"""
    model_config = ConfigDict(from_attributes=True)
    
    id: UUID
    user_id: UUID
    bank_name: str
    account_type: Optional[str]
    iban: Optional[str]
    balance: Decimal
    currency: str
    is_active: bool
    last_sync_at: Optional[datetime]
    sync_error: Optional[str]
    created_at: datetime
    updated_at: datetime


class BankAccountList(BaseModel):
    """Schema for list of bank accounts"""
    accounts: list[BankAccountRead]
    total: int


