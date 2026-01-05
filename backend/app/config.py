"""Application configuration - International-ready"""
from pydantic_settings import BaseSettings
from typing import List


class Settings(BaseSettings):
    """
    Application settings with international support
    
    All settings can be overridden via environment variables
    """
    
    # Application
    APP_NAME: str = "FinanceAI"
    APP_ENV: str = "development"
    DEBUG: bool = True
    
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
    
    # CORS (multiple origins for international domains)
    CORS_ORIGINS: str = "http://localhost:3000,http://localhost:3001"
    
    @property
    def cors_origins_list(self) -> List[str]:
        return [origin.strip() for origin in self.CORS_ORIGINS.split(",")]
    
    # Internationalization
    DEFAULT_LANGUAGE: str = "fr"
    SUPPORTED_LANGUAGES: str = "fr,en,es,de,it,nl"
    
    @property
    def supported_languages_list(self) -> List[str]:
        return [lang.strip() for lang in self.SUPPORTED_LANGUAGES.split(",")]
    
    DEFAULT_CURRENCY: str = "EUR"
    SUPPORTED_CURRENCIES: str = "EUR,USD,GBP,CHF,CAD"
    
    @property
    def supported_currencies_list(self) -> List[str]:
        return [curr.strip() for curr in self.SUPPORTED_CURRENCIES.split(",")]
    
    DEFAULT_TIMEZONE: str = "Europe/Paris"
    
    # Supported countries (for banking integrations and legal)
    SUPPORTED_COUNTRIES: str = "FR,BE,CH,LU,ES,DE,IT,NL,GB,US,CA"
    
    @property
    def supported_countries_list(self) -> List[str]:
        return [country.strip() for country in self.SUPPORTED_COUNTRIES.split(",")]
    
    # Bridge API (Banking) - Works in 11+ European countries
    BRIDGE_ENV: str = "sandbox"  # sandbox or production
    BRIDGE_CLIENT_ID: str
    BRIDGE_CLIENT_SECRET: str
    BRIDGE_API_KEY: str
    BRIDGE_API_URL: str = "https://api.bridgeapi.io/v2"
    
    # Bridge supported countries
    # FR, BE, ES, DE, IT, PT, NL, AT, IE, PL, LU
    BRIDGE_SUPPORTED_COUNTRIES: List[str] = [
        "FR", "BE", "ES", "DE", "IT", "PT", "NL", "AT", "IE", "PL", "LU"
    ]
    
    # Future: Add other banking providers
    # PLAID_CLIENT_ID: str = ""  # For US/CA
    # TRUELAYER_CLIENT_ID: str = ""  # For UK
    
    # Anthropic Claude (AI)
    ANTHROPIC_API_KEY: str
    ANTHROPIC_MODEL: str = "claude-3-5-sonnet-20241022"
    
    # OpenAI (optional fallback)
    OPENAI_API_KEY: str = ""
    OPENAI_MODEL: str = "gpt-4o-mini"
    
    # SendGrid (Email) - International support
    SENDGRID_API_KEY: str
    SENDGRID_FROM_EMAIL: str = "noreply@financeai.fr"
    SENDGRID_FROM_NAME: str = "FinanceAI"
    
    # Stripe (Payments) - Global support
    STRIPE_PUBLIC_KEY: str
    STRIPE_SECRET_KEY: str
    STRIPE_WEBHOOK_SECRET: str
    
    # Stripe supports 135+ currencies
    # Automatic currency detection based on user's country
    
    # Currency Exchange Rates API (for multi-currency conversion)
    EXCHANGE_RATE_API_KEY: str = ""
    EXCHANGE_RATE_API_URL: str = "https://api.exchangerate-api.com/v4/latest/"
    
    # Sentry (Error Tracking)
    SENTRY_DSN: str = ""
    
    # Logging
    LOG_LEVEL: str = "INFO"
    LOG_FORMAT: str = "json"  # json or text
    
    # Feature Flags (easy to enable/disable features per market)
    FEATURE_BANK_SYNC: bool = True
    FEATURE_AI_CATEGORIZATION: bool = True
    FEATURE_AUTO_RECONCILIATION: bool = True
    FEATURE_PAYMENT_REMINDERS: bool = True
    FEATURE_CASH_FLOW_FORECAST: bool = False  # Coming soon
    
    # Market-specific features
    FEATURE_FR_ACCOUNTING_EXPORT: bool = True  # French accounting standards
    FEATURE_CH_VAT_RATES: bool = False  # Swiss VAT rates (enable when needed)
    FEATURE_US_TAX_FORMS: bool = False  # US tax forms (future)
    
    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()

