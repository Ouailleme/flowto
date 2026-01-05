"""Bank Account model for storing connected bank accounts"""
from sqlalchemy import Column, String, DateTime, Boolean, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from app.core.database import Base
import uuid
from datetime import datetime


class BankAccount(Base):
    """Bank account connected via Bridge API"""
    __tablename__ = "bank_accounts"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    bridge_account_id = Column(String(255), unique=True, nullable=False, index=True)
    bridge_item_id = Column(String(255), nullable=False, index=True)
    bank_name = Column(String(255), nullable=False)
    account_name = Column(String(255), nullable=True)
    account_type = Column(String(50), nullable=True)
    iban = Column(String(100), nullable=True)
    currency = Column(String(3), nullable=False, default="EUR")
    is_active = Column(Boolean, default=True)
    last_sync_at = Column(DateTime(timezone=True), nullable=True)
    created_at = Column(DateTime(timezone=True), default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime(timezone=True), default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    deleted_at = Column(DateTime(timezone=True), nullable=True)
    
    # Relationships
    transactions = relationship("Transaction", back_populates="bank_account", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<BankAccount {self.bank_name} - {self.account_name}>"
