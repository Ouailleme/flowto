"""User model - International-ready from Day 1"""
from sqlalchemy import Column, String, DateTime, Boolean, Enum
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from app.core.database import Base
import uuid
from datetime import datetime
import enum


class LanguageEnum(str, enum.Enum):
    """Supported languages - Easy to add more"""
    FRENCH = "fr"
    ENGLISH = "en"
    SPANISH = "es"
    GERMAN = "de"
    ITALIAN = "it"
    DUTCH = "nl"


class CurrencyEnum(str, enum.Enum):
    """Supported currencies - Easy to add more"""
    EUR = "EUR"
    USD = "USD"
    GBP = "GBP"
    CHF = "CHF"
    CAD = "CAD"


class CountryEnum(str, enum.Enum):
    """Supported countries - Easy to add more"""
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
    """
    User model - International-ready
    
    Supports:
    - Multiple languages
    - Multiple currencies
    - Multiple countries
    - Multiple timezones
    """
    __tablename__ = "users"
    
    # Core fields
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    email = Column(String(255), unique=True, nullable=False, index=True)
    hashed_password = Column(String(255), nullable=False)
    
    # Company info
    company_name = Column(String(255), nullable=False)
    company_size = Column(String(50))  # "1-10", "10-50", "50-200", "200+"
    
    # International settings
    language = Column(
        Enum(LanguageEnum),
        nullable=False,
        default=LanguageEnum.FRENCH,
        comment="User's preferred language for interface and emails"
    )
    country = Column(
        Enum(CountryEnum),
        nullable=False,
        default=CountryEnum.FRANCE,
        comment="User's country (for legal, tax, banking integrations)"
    )
    currency = Column(
        Enum(CurrencyEnum),
        nullable=False,
        default=CurrencyEnum.EUR,
        comment="User's preferred currency for display and billing"
    )
    timezone = Column(
        String(50),
        nullable=False,
        default="Europe/Paris",
        comment="User's timezone (e.g. 'Europe/Paris', 'America/New_York')"
    )
    
    # Locale settings (for number/date formatting)
    locale = Column(
        String(10),
        nullable=False,
        default="fr_FR",
        comment="Locale for formatting (e.g. 'fr_FR', 'en_US', 'de_DE')"
    )
    
    # Subscription
    subscription_plan = Column(
        String(50),
        default="trial",
        comment="trial, starter, pro, business"
    )
    subscription_status = Column(
        String(50),
        default="active",
        comment="active, cancelled, expired, past_due"
    )
    stripe_customer_id = Column(String(255), unique=True, nullable=True)
    
    # Account status
    is_active = Column(Boolean, default=True)
    is_verified = Column(Boolean, default=False)
    is_onboarded = Column(Boolean, default=False, comment="Has completed onboarding flow")
    
    # Timestamps
    created_at = Column(
        DateTime(timezone=True),
        default=datetime.utcnow,
        nullable=False
    )
    updated_at = Column(
        DateTime(timezone=True),
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
        nullable=False
    )
    deleted_at = Column(DateTime(timezone=True), nullable=True)
    
    # Relationships
    bank_accounts = relationship("BankAccount", back_populates="user", cascade="all, delete-orphan")
    invoices = relationship("Invoice", back_populates="user", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<User {self.email} ({self.country.value})>"

