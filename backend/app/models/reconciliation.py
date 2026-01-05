"""Reconciliation model for matching transactions with invoices"""
from sqlalchemy import Column, String, DateTime, Numeric, Text, ForeignKey, Boolean
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from app.core.database import Base
import uuid
from datetime import datetime


class Reconciliation(Base):
    """Reconciliation record linking transactions to invoices"""
    __tablename__ = "reconciliations"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    transaction_id = Column(UUID(as_uuid=True), ForeignKey("transactions.id", ondelete="CASCADE"), nullable=False, unique=True, index=True)
    invoice_id = Column(UUID(as_uuid=True), ForeignKey("invoices.id", ondelete="CASCADE"), nullable=False, index=True)
    confidence_score = Column(Numeric(5, 2), nullable=False)
    match_type = Column(String(50), nullable=False)
    is_validated = Column(Boolean, default=False)
    validated_by = Column(UUID(as_uuid=True), nullable=True)
    validated_at = Column(DateTime(timezone=True), nullable=True)
    ai_reasoning = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime(timezone=True), default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    
    # Relationships
    transaction = relationship("Transaction", back_populates="reconciliation")
    invoice = relationship("Invoice", back_populates="reconciliation")
    
    def __repr__(self):
        return f"<Reconciliation Transaction {self.transaction_id} <-> Invoice {self.invoice_id} ({self.confidence_score}%)>"
