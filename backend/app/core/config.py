"""
Application configuration using Pydantic Settings.
Loads settings from environment variables and .env file.
"""
from typing import Optional
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """
    Application settings.
    All settings can be overridden by environment variables.
    """
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )
    
    # Application
    app_name: str = "Flowto API"
    app_version: str = "1.0.0"
    debug: bool = False
    
    # Database
    database_url: str = "postgresql+asyncpg://financeai:financeai2026@postgres:5432/financeai"
    
    # Redis & Celery
    redis_url: str = "redis://redis:6379/0"
    celery_broker_url: str = "redis://redis:6379/0"
    celery_result_backend: str = "redis://redis:6379/1"
    
    # Security
    secret_key: str = "your-secret-key-change-in-production-min-32-chars"
    access_token_expire_minutes: int = 60  # 1 hour
    refresh_token_expire_days: int = 30  # 30 days
    algorithm: str = "HS256"
    
    # CORS
    cors_origins: str = "http://localhost:3000,http://localhost:8000,https://flowto.fr"
    
    @property
    def cors_origins_list(self) -> list[str]:
        """Parse CORS origins from comma-separated string to list."""
        return [origin.strip() for origin in self.cors_origins.split(",")]
    
    # External APIs
    bridge_api_key: Optional[str] = None
    bridge_api_url: str = "https://api.bridgeapi.io/v2"
    
    anthropic_api_key: Optional[str] = None
    
    sendgrid_api_key: Optional[str] = None
    sendgrid_from_email: str = "noreply@flowto.fr"
    
    # Logging
    log_level: str = "INFO"
    log_format: str = "json"  # or "text"
    
    # Sentry (Error tracking)
    sentry_dsn: Optional[str] = None
    sentry_environment: str = "development"
    
    # Application limits
    max_invoice_amount: float = 100000.00
    max_transactions_per_sync: int = 1000
    
    # Feature flags
    enable_ai_categorization: bool = True
    enable_auto_reconciliation: bool = True
    enable_email_reminders: bool = True


# Global settings instance
settings = Settings()

