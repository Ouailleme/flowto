"""Transaction model for bank transactions"""
from sqlalchemy import Column, String, DateTime, Numeric, Boolean, Text, ForeignKey, CheckConstraint
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from app.core.database import Base
import uuid
from datetime import datetime


class Transaction(Base):
    """Bank transaction from Bridge API"""
    __tablename__ = "transactions"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    bank_account_id = Column(UUID(as_uuid=True), ForeignKey("bank_accounts.id", ondelete="CASCADE"), nullable=False, index=True)
    bridge_transaction_id = Column(String(255), unique=True, nullable=False, index=True)
    description = Column(Text, nullable=False)
    amount = Column(Numeric(15, 2), nullable=False)
    currency = Column(String(3), nullable=False, default="EUR")
    date = Column(DateTime(timezone=True), nullable=False, index=True)
    category = Column(String(100), nullable=True, index=True)
    is_recurring = Column(Boolean, default=False)
    is_reconciled = Column(Boolean, default=False, index=True)
    reconciled_invoice_id = Column(UUID(as_uuid=True), nullable=True, index=True)
    raw_data = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime(timezone=True), default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    deleted_at = Column(DateTime(timezone=True), nullable=True)
    
    # Relationships
    bank_account = relationship("BankAccount", back_populates="transactions")
    reconciliation = relationship("Reconciliation", back_populates="transaction", uselist=False)
    
    # Constraints
    __table_args__ = (
        CheckConstraint('amount != 0', name='check_amount_not_zero'),
    )
    
    def __repr__(self):
        return f"<Transaction {self.description[:30]} - {self.amount} {self.currency}>"
