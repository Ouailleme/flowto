"""Invoice model for customer invoices"""
from sqlalchemy import Column, String, DateTime, Numeric, Date, Text, Boolean, ForeignKey, CheckConstraint
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from app.core.database import Base
import uuid
from datetime import datetime


class Invoice(Base):
    """Customer invoice"""
    __tablename__ = "invoices"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    invoice_number = Column(String(50), nullable=False, index=True)
    client_name = Column(String(255), nullable=False, index=True)
    client_email = Column(String(255), nullable=True)
    client_address = Column(Text, nullable=True)
    amount = Column(Numeric(15, 2), nullable=False)
    tax_amount = Column(Numeric(15, 2), nullable=False, default=0)
    total_amount = Column(Numeric(15, 2), nullable=False)
    currency = Column(String(3), nullable=False, default="EUR")
    issue_date = Column(Date, nullable=False, index=True)
    due_date = Column(Date, nullable=False, index=True)
    payment_date = Column(Date, nullable=True, index=True)
    status = Column(String(50), nullable=False, default="pending", index=True)
    is_reconciled = Column(Boolean, nullable=False, default=False)
    description = Column(Text, nullable=True)
    notes = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime(timezone=True), default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    deleted_at = Column(DateTime(timezone=True), nullable=True)
    
    # Relationships
    reconciliation = relationship("Reconciliation", back_populates="invoice", uselist=False)
    reminders = relationship("Reminder", back_populates="invoice", cascade="all, delete-orphan")
    
    # Constraints
    __table_args__ = (
        CheckConstraint('amount > 0', name='check_amount_positive'),
        CheckConstraint("status IN ('pending', 'paid', 'overdue', 'cancelled')", name='check_status_valid'),
    )
    
    def __repr__(self):
        return f"<Invoice {self.invoice_number} - {self.client_name} - {self.amount} {self.currency}>"
