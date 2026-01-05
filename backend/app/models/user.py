"""Simplified User model for authentication - No relationships"""
from sqlalchemy import Column, String, DateTime, Boolean
from sqlalchemy.dialects.postgresql import UUID
from app.core.database import Base
import uuid
from datetime import datetime
import enum


# Enums needed for compatibility with other modules
class LanguageEnum(str, enum.Enum):
    """Supported languages"""
    FRENCH = "fr"
    ENGLISH = "en"
    SPANISH = "es"
    GERMAN = "de"
    ITALIAN = "it"
    DUTCH = "nl"


class CurrencyEnum(str, enum.Enum):
    """Supported currencies"""
    EUR = "EUR"
    USD = "USD"
    GBP = "GBP"
    CHF = "CHF"
    CAD = "CAD"


class CountryEnum(str, enum.Enum):
    """Supported countries"""
    FRANCE = "FR"
    BELGIUM = "BE"
    SWITZERLAND = "CH"
    LUXEMBOURG = "LU"
    SPAIN = "ES"
    GERMANY = "DE"
    ITALY = "IT"
    NETHERLANDS = "NL"
    UK = "GB"
    USA = "US"
    CANADA = "CA"


class User(Base):
    """Simplified User model for MVP authentication"""
    __tablename__ = "users"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    email = Column(String(255), unique=True, nullable=False, index=True)
    hashed_password = Column(String(255), nullable=False)
    full_name = Column(String(255), nullable=True)
    is_active = Column(Boolean, default=True)
    is_verified = Column(Boolean, default=False)
    is_superuser = Column(Boolean, default=False)
    language = Column(String(10), default="fr")
    country = Column(String(10), default="FR")
    currency = Column(String(10), default="EUR")
    timezone = Column(String(50), default="Europe/Paris")
    locale = Column(String(10), default="fr_FR")
    company_name = Column(String(255), nullable=True)
    company_size = Column(String(50), nullable=True)
    industry = Column(String(100), nullable=True)
    subscription_plan = Column(String(50), default="trial")
    subscription_status = Column(String(50), default="active")
    stripe_customer_id = Column(String(255), nullable=True)
    is_onboarded = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime(timezone=True), default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    deleted_at = Column(DateTime(timezone=True), nullable=True)
    last_login_at = Column(DateTime(timezone=True), nullable=True)
    email_verified_at = Column(DateTime(timezone=True), nullable=True)
    
    def __repr__(self):
        return f"<User {self.email}>"

