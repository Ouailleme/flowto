"""Application configuration - Simplified for MVP"""
from pydantic_settings import BaseSettings
from typing import List, Optional
from enum import Enum


# Internationalization Enums
class LanguageEnum(str, Enum):
    FRENCH = "fr"
    ENGLISH = "en"
    SPANISH = "es"
    GERMAN = "de"
    ITALIAN = "it"
    DUTCH = "nl"


class CountryEnum(str, Enum):
    FRANCE = "FR"
    BELGIUM = "BE"
    SWITZERLAND = "CH"
    LUXEMBOURG = "LU"
    SPAIN = "ES"
    GERMANY = "DE"
    ITALY = "IT"
    NETHERLANDS = "NL"
    UNITED_KINGDOM = "GB"
    USA = "US"
    CANADA = "CA"


class CurrencyEnum(str, Enum):
    EUR = "EUR"
    USD = "USD"
    GBP = "GBP"
    CHF = "CHF"
    CAD = "CAD"


class Settings(BaseSettings):
    """Application settings"""
    
    # Application
    APP_NAME: str = "FinanceAI"
    APP_ENV: str = "development"
    DEBUG: bool = True
    VERSION: str = "1.0.0"
    
    # Security
    SECRET_KEY: str
    JWT_SECRET_KEY: str
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7
    
    # Database
    DATABASE_URL: str
    
    # Redis
    REDIS_URL: str = "redis://localhost:6379/0"
    
    # Celery
    CELERY_BROKER_URL: str = "redis://localhost:6379/0"
    CELERY_RESULT_BACKEND: str = "redis://localhost:6379/0"
    
    # CORS
    CORS_ORIGINS: str = "http://localhost:3000,http://localhost:3001"
    
    @property
    def cors_origins_list(self) -> List[str]:
        return [origin.strip() for origin in self.CORS_ORIGINS.split(",")]
    
    # Internationalization
    DEFAULT_LANGUAGE: str = "fr"
    SUPPORTED_LANGUAGES: str = "fr,en,es,de,it,nl"
    DEFAULT_CURRENCY: str = "EUR"
    SUPPORTED_CURRENCIES: str = "EUR,USD,GBP,CHF,CAD"
    DEFAULT_COUNTRY: str = "FR"
    SUPPORTED_COUNTRIES: str = "FR,BE,CH,LU,ES,DE,IT,NL,GB,US,CA"
    DEFAULT_TIMEZONE: str = "Europe/Paris"
    
    @property
    def supported_languages_list(self) -> List[str]:
        return [lang.strip() for lang in self.SUPPORTED_LANGUAGES.split(",")]
    
    @property
    def supported_currencies_list(self) -> List[str]:
        return [curr.strip() for curr in self.SUPPORTED_CURRENCIES.split(",")]
    
    @property
    def supported_countries_list(self) -> List[str]:
        return [country.strip() for country in self.SUPPORTED_COUNTRIES.split(",")]
    
    # API Settings
    API_V1_STR: str = "/api/v1"
    
    # External APIs (Optional for MVP)
    BRIDGE_API_KEY: Optional[str] = None
    BRIDGE_CLIENT_ID: Optional[str] = None
    BRIDGE_CLIENT_SECRET: Optional[str] = None
    CLAUDE_API_KEY: Optional[str] = None
    SENDGRID_API_KEY: Optional[str] = None
    EXCHANGE_RATE_API_KEY: Optional[str] = None
    STRIPE_PUBLIC_KEY: Optional[str] = None
    STRIPE_SECRET_KEY: Optional[str] = None
    STRIPE_WEBHOOK_SECRET: Optional[str] = None
    
    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()
