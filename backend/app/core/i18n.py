"""Internationalization utilities"""
from typing import Dict, Optional
from datetime import datetime
import babel.dates
import babel.numbers
from decimal import Decimal


class I18n:
    """
    Internationalization helper
    
    Handles:
    - Date/time formatting
    - Number formatting
    - Currency formatting
    - Translations (basic, will use proper i18n later)
    """
    
    # Language to locale mapping
    LOCALE_MAP = {
        "fr": "fr_FR",
        "en": "en_US",
        "es": "es_ES",
        "de": "de_DE",
        "it": "it_IT",
        "nl": "nl_NL",
    }
    
    # Timezone to country mapping (approximate)
    TIMEZONE_COUNTRY_MAP = {
        "Europe/Paris": "FR",
        "Europe/Brussels": "BE",
        "Europe/Zurich": "CH",
        "Europe/Luxembourg": "LU",
        "Europe/Madrid": "ES",
        "Europe/Berlin": "DE",
        "Europe/Rome": "IT",
        "Europe/Amsterdam": "NL",
        "Europe/London": "GB",
        "America/New_York": "US",
        "America/Toronto": "CA",
    }
    
    @staticmethod
    def get_locale(language: str) -> str:
        """Get locale from language code"""
        return I18n.LOCALE_MAP.get(language, "en_US")
    
    @staticmethod
    def format_date(
        date: datetime,
        language: str = "fr",
        format: str = "medium"
    ) -> str:
        """
        Format date according to locale
        
        Examples:
        - fr: "5 janv. 2026"
        - en: "Jan 5, 2026"
        - de: "5. Jan. 2026"
        """
        locale = I18n.get_locale(language)
        return babel.dates.format_date(date, format=format, locale=locale)
    
    @staticmethod
    def format_datetime(
        dt: datetime,
        language: str = "fr",
        format: str = "medium",
        timezone: str = "Europe/Paris"
    ) -> str:
        """
        Format datetime according to locale and timezone
        
        Examples:
        - fr: "5 janv. 2026 à 14:30"
        - en: "Jan 5, 2026, 2:30 PM"
        """
        locale = I18n.get_locale(language)
        return babel.dates.format_datetime(
            dt,
            format=format,
            tzinfo=timezone,
            locale=locale
        )
    
    @staticmethod
    def format_number(
        number: float | Decimal,
        language: str = "fr"
    ) -> str:
        """
        Format number according to locale
        
        Examples:
        - fr: "1 234,56"
        - en: "1,234.56"
        - de: "1.234,56"
        """
        locale = I18n.get_locale(language)
        return babel.numbers.format_decimal(number, locale=locale)
    
    @staticmethod
    def format_currency(
        amount: float | Decimal,
        currency: str = "EUR",
        language: str = "fr"
    ) -> str:
        """
        Format currency according to locale
        
        Examples:
        - fr + EUR: "1 234,56 €"
        - en + USD: "$1,234.56"
        - de + CHF: "CHF 1'234.56"
        """
        locale = I18n.get_locale(language)
        return babel.numbers.format_currency(
            amount,
            currency,
            locale=locale
        )
    
    @staticmethod
    def format_percent(
        number: float,
        language: str = "fr"
    ) -> str:
        """
        Format percentage according to locale
        
        Examples:
        - fr: "12,5 %"
        - en: "12.5%"
        """
        locale = I18n.get_locale(language)
        return babel.numbers.format_percent(number, locale=locale)


# Translations (basic version - will use proper i18n system later)
TRANSLATIONS: Dict[str, Dict[str, str]] = {
    # Email subjects
    "email.reminder.subject": {
        "fr": "Rappel de paiement - Facture {invoice_number}",
        "en": "Payment Reminder - Invoice {invoice_number}",
        "es": "Recordatorio de pago - Factura {invoice_number}",
        "de": "Zahlungserinnerung - Rechnung {invoice_number}",
    },
    
    # Transaction categories
    "category.salaires": {
        "fr": "Salaires",
        "en": "Salaries",
        "es": "Salarios",
        "de": "Gehälter",
    },
    "category.loyer": {
        "fr": "Loyer",
        "en": "Rent",
        "es": "Alquiler",
        "de": "Miete",
    },
    "category.clients": {
        "fr": "Clients",
        "en": "Customers",
        "es": "Clientes",
        "de": "Kunden",
    },
    
    # UI strings
    "ui.dashboard": {
        "fr": "Tableau de bord",
        "en": "Dashboard",
        "es": "Panel de control",
        "de": "Dashboard",
    },
    "ui.transactions": {
        "fr": "Transactions",
        "en": "Transactions",
        "es": "Transacciones",
        "de": "Transaktionen",
    },
    "ui.invoices": {
        "fr": "Factures",
        "en": "Invoices",
        "es": "Facturas",
        "de": "Rechnungen",
    },
}


def t(key: str, language: str = "fr", **kwargs) -> str:
    """
    Translate a key to the given language
    
    Usage:
        t("email.reminder.subject", "en", invoice_number="F001")
        # → "Payment Reminder - Invoice F001"
    """
    translations = TRANSLATIONS.get(key, {})
    text = translations.get(language) or translations.get("en") or key
    
    # Replace placeholders
    if kwargs:
        text = text.format(**kwargs)
    
    return text

