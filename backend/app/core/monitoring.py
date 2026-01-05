"""
Monitoring configuration with Sentry and structured logging.
"""
import logging
import sys
from typing import Optional

try:
    import sentry_sdk
    from sentry_sdk.integrations.fastapi import FastApiIntegration
    from sentry_sdk.integrations.sqlalchemy import SqlalchemyIntegration
    from sentry_sdk.integrations.redis import RedisIntegration
    from sentry_sdk.integrations.logging import LoggingIntegration
    SENTRY_AVAILABLE = True
except ImportError:
    SENTRY_AVAILABLE = False

try:
    import structlog
    STRUCTLOG_AVAILABLE = True
except ImportError:
    STRUCTLOG_AVAILABLE = False

from app.core.config import settings


def setup_sentry() -> None:
    """Initialize Sentry for error tracking."""
    if not SENTRY_AVAILABLE:
        logging.warning("Sentry SDK not installed. Install with: pip install sentry-sdk")
        return
    
    if not settings.sentry_dsn:
        logging.info("Sentry DSN not configured. Skipping Sentry initialization.")
        return
    
    sentry_sdk.init(
        dsn=settings.sentry_dsn,
        environment=settings.sentry_environment,
        release=f"flowto-backend@{settings.app_version}",
        traces_sample_rate=0.1,  # 10% of transactions for performance monitoring
        profiles_sample_rate=0.1,  # 10% for profiling
        integrations=[
            FastApiIntegration(transaction_style="endpoint"),
            SqlalchemyIntegration(),
            RedisIntegration(),
            LoggingIntegration(
                level=logging.INFO,  # Capture info and above as breadcrumbs
                event_level=logging.ERROR  # Send errors as events
            ),
        ],
        # Filter sensitive data
        before_send=before_send_sentry,
        # Performance monitoring
        enable_tracing=True,
    )
    
    logging.info(f"Sentry initialized for environment: {settings.sentry_environment}")


def before_send_sentry(event, hint):
    """
    Filter sensitive data before sending to Sentry.
    Remove passwords, tokens, API keys, etc.
    """
    # Remove sensitive headers
    if "request" in event and "headers" in event["request"]:
        headers = event["request"]["headers"]
        sensitive_headers = ["authorization", "cookie", "x-api-key"]
        for header in sensitive_headers:
            if header in headers:
                headers[header] = "[Filtered]"
    
    # Remove sensitive query parameters
    if "request" in event and "query_string" in event["request"]:
        query = event["request"]["query_string"]
        if "password" in query or "token" in query:
            event["request"]["query_string"] = "[Filtered]"
    
    # Remove sensitive data from extra context
    if "extra" in event:
        sensitive_keys = ["password", "token", "api_key", "secret", "iban"]
        for key in sensitive_keys:
            if key in event["extra"]:
                event["extra"][key] = "[Filtered]"
    
    return event


def setup_structured_logging() -> None:
    """
    Configure structured logging with structlog (JSON format).
    Falls back to standard logging if structlog not available.
    """
    if STRUCTLOG_AVAILABLE:
        structlog.configure(
            processors=[
                structlog.stdlib.filter_by_level,
                structlog.stdlib.add_logger_name,
                structlog.stdlib.add_log_level,
                structlog.stdlib.PositionalArgumentsFormatter(),
                structlog.processors.TimeStamper(fmt="iso"),
                structlog.processors.StackInfoRenderer(),
                structlog.processors.format_exc_info,
                structlog.processors.UnicodeDecoder(),
                structlog.processors.JSONRenderer()  # JSON output
            ],
            context_class=dict,
            logger_factory=structlog.stdlib.LoggerFactory(),
            cache_logger_on_first_use=True,
        )
        logging.info("Structured logging (structlog) initialized with JSON format")
    else:
        # Fallback to standard logging with JSON-like format
        logging.basicConfig(
            level=logging.INFO if settings.sentry_environment == "production" else logging.DEBUG,
            format='{"timestamp": "%(asctime)s", "level": "%(levelname)s", "logger": "%(name)s", "message": "%(message)s"}',
            handlers=[
                logging.StreamHandler(sys.stdout)
            ]
        )
        logging.warning("structlog not installed. Using standard logging. Install with: pip install structlog")


def get_logger(name: str):
    """
    Get a logger instance (structlog or standard).
    
    Args:
        name: Logger name (usually __name__)
        
    Returns:
        Logger instance
    """
    if STRUCTLOG_AVAILABLE:
        return structlog.get_logger(name)
    else:
        return logging.getLogger(name)


def log_request(
    method: str,
    path: str,
    status_code: int,
    duration_ms: float,
    user_id: Optional[str] = None
) -> None:
    """
    Log HTTP request with structured data.
    
    Args:
        method: HTTP method (GET, POST, etc.)
        path: Request path
        status_code: Response status code
        duration_ms: Request duration in milliseconds
        user_id: Optional user ID
    """
    logger = get_logger("flowto.api")
    
    log_data = {
        "event": "http_request",
        "method": method,
        "path": path,
        "status_code": status_code,
        "duration_ms": duration_ms,
    }
    
    if user_id:
        log_data["user_id"] = user_id
    
    if STRUCTLOG_AVAILABLE:
        logger.info("HTTP request", **log_data)
    else:
        logger.info(f"HTTP request: {log_data}")


def log_error(
    error: Exception,
    context: dict,
    user_id: Optional[str] = None
) -> None:
    """
    Log error with context.
    
    Args:
        error: Exception instance
        context: Additional context (endpoint, operation, etc.)
        user_id: Optional user ID
    """
    logger = get_logger("flowto.errors")
    
    log_data = {
        "event": "error",
        "error_type": type(error).__name__,
        "error_message": str(error),
        **context
    }
    
    if user_id:
        log_data["user_id"] = user_id
    
    if STRUCTLOG_AVAILABLE:
        logger.error("Application error", **log_data, exc_info=True)
    else:
        logger.error(f"Application error: {log_data}", exc_info=True)

