"""Transaction model - Multi-currency support"""
from sqlalchemy import Column, String, DateTime, Boolean, Numeric, ForeignKey, Index
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from app.core.database import Base
import uuid
from datetime import datetime


class Transaction(Base):
    """
    Bank transaction model
    
    Multi-currency support:
    - All amounts stored with their original currency
    - Conversion to user's preferred currency done at display time
    """
    __tablename__ = "transactions"
    
    # Core fields
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    bank_account_id = Column(
        UUID(as_uuid=True),
        ForeignKey("bank_accounts.id", ondelete="CASCADE"),
        nullable=False,
        index=True
    )
    
    # External ID (from Bridge API or other banking provider)
    bridge_transaction_id = Column(String(255), unique=True, nullable=True, index=True)
    external_id = Column(
        String(255),
        nullable=True,
        comment="Transaction ID from any external provider (Bridge, Plaid, TrueLayer, etc.)"
    )
    
    # Transaction details
    date = Column(DateTime(timezone=True), nullable=False, index=True)
    description = Column(String(500), nullable=False)
    
    # Multi-currency amount
    amount = Column(
        Numeric(15, 2),
        nullable=False,
        comment="Transaction amount in original currency"
    )
    currency = Column(
        String(3),
        nullable=False,
        default="EUR",
        comment="ISO 4217 currency code (EUR, USD, GBP, CHF, etc.)"
    )
    
    # Converted amount (to user's preferred currency)
    amount_converted = Column(
        Numeric(15, 2),
        nullable=True,
        comment="Amount converted to user's preferred currency (if different)"
    )
    conversion_rate = Column(
        Numeric(10, 6),
        nullable=True,
        comment="Exchange rate used for conversion"
    )
    conversion_date = Column(
        DateTime(timezone=True),
        nullable=True,
        comment="Date of currency conversion"
    )
    
    # Transaction type
    transaction_type = Column(
        String(50),
        nullable=True,
        comment="debit, credit, transfer, fee, etc."
    )
    
    # AI Categorization
    category = Column(
        String(100),
        nullable=True,
        index=True,
        comment="AI-assigned category (Salaires, Fournitures, Loyer, etc.)"
    )
    category_confidence = Column(
        Numeric(3, 2),
        nullable=True,
        comment="AI confidence score (0.00 to 1.00)"
    )
    
    # Reconciliation
    is_reconciled = Column(Boolean, default=False, nullable=False, index=True)
    reconciliation_id = Column(
        UUID(as_uuid=True),
        ForeignKey("reconciliations.id", ondelete="SET NULL"),
        nullable=True
    )
    
    # Metadata
    raw_data = Column(
        String,
        nullable=True,
        comment="JSON string of raw transaction data from provider"
    )
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), default=datetime.utcnow, nullable=False)
    updated_at = Column(
        DateTime(timezone=True),
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
        nullable=False
    )
    deleted_at = Column(DateTime(timezone=True), nullable=True)
    
    # Relationships
    bank_account = relationship("BankAccount", back_populates="transactions")
    reconciliation = relationship("Reconciliation", back_populates="transaction")
    
    # Indexes for performance
    __table_args__ = (
        Index("idx_transaction_date_amount", "date", "amount"),
        Index("idx_transaction_currency", "currency"),
        Index("idx_transaction_category", "category"),
    )
    
    def __repr__(self):
        return f"<Transaction {self.date} {self.amount} {self.currency}>"

