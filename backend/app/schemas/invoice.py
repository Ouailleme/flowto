"""Invoice Pydantic schemas"""
from pydantic import BaseModel, EmailStr, Field, field_validator, ConfigDict
from uuid import UUID
from datetime import date, datetime
from decimal import Decimal
from typing import Optional


class InvoiceCreate(BaseModel):
    """Schema for creating an invoice"""
    invoice_number: str = Field(..., min_length=1, max_length=100)
    client_name: str = Field(..., min_length=1, max_length=255)
    client_email: Optional[EmailStr] = None
    client_address: Optional[str] = Field(None, max_length=500)
    amount: Decimal = Field(..., gt=0)
    tax_amount: Decimal = Field(default=Decimal("0.00"), ge=0)
    currency: str = Field(default="EUR", min_length=3, max_length=3)
    issue_date: date
    due_date: date
    description: Optional[str] = Field(None, max_length=1000)
    notes: Optional[str] = Field(None, max_length=1000)
    
    @field_validator("due_date")
    @classmethod
    def due_date_after_issue(cls, v: date, info) -> date:
        """Validate due_date is after issue_date"""
        issue_date = info.data.get("issue_date")
        if issue_date and v < issue_date:
            raise ValueError("Due date must be after issue date")
        return v
    
    @property
    def total_amount(self) -> Decimal:
        """Calculate total amount"""
        return self.amount + self.tax_amount
    
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "invoice_number": "INV-2026-001",
                "client_name": "ACME Corp",
                "client_email": "billing@acme.com",
                "amount": 2500.00,
                "tax_amount": 500.00,
                "currency": "EUR",
                "issue_date": "2026-01-05",
                "due_date": "2026-02-05",
                "description": "Services de conseil janvier 2026"
            }
        }
    )


class InvoiceUpdate(BaseModel):
    """Schema for updating invoice"""
    client_name: Optional[str] = Field(None, min_length=1, max_length=255)
    client_email: Optional[EmailStr] = None
    client_address: Optional[str] = Field(None, max_length=500)
    amount: Optional[Decimal] = Field(None, gt=0)
    tax_amount: Optional[Decimal] = Field(None, ge=0)
    due_date: Optional[date] = None
    status: Optional[str] = Field(None, pattern="^(pending|paid|overdue|cancelled)$")
    description: Optional[str] = Field(None, max_length=1000)
    notes: Optional[str] = Field(None, max_length=1000)


class InvoiceRead(BaseModel):
    """Schema for reading invoice (response)"""
    model_config = ConfigDict(from_attributes=True)
    
    id: UUID
    user_id: UUID
    invoice_number: str
    client_name: str
    client_email: Optional[str]
    amount: Decimal
    tax_amount: Decimal
    total_amount: Decimal
    currency: str
    issue_date: date
    due_date: date
    payment_date: Optional[date]
    status: str
    is_reconciled: bool
    description: Optional[str]
    notes: Optional[str]
    created_at: datetime
    updated_at: datetime


class InvoiceFilter(BaseModel):
    """Schema for filtering invoices"""
    status: Optional[str] = Field(None, pattern="^(pending|paid|overdue|cancelled)$")
    is_reconciled: Optional[bool] = None
    start_date: Optional[date] = None
    end_date: Optional[date] = None
    client_name: Optional[str] = Field(None, max_length=255)
    min_amount: Optional[Decimal] = None
    max_amount: Optional[Decimal] = None


class InvoiceList(BaseModel):
    """Schema for list of invoices with pagination"""
    invoices: list[InvoiceRead]
    total: int
    page: int
    page_size: int
    total_pages: int


