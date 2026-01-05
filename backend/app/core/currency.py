"""Currency conversion utilities"""
import httpx
from decimal import Decimal
from datetime import datetime, timedelta
from typing import Dict, Optional
import asyncio
from app.config import settings


class CurrencyConverter:
    """
    Currency conversion with caching
    
    Supports:
    - Real-time exchange rates
    - Caching (1 hour)
    - Fallback to cached rates if API fails
    """
    
    # Cache for exchange rates (in-memory, will use Redis in production)
    _cache: Dict[str, Dict] = {}
    _cache_timestamp: Optional[datetime] = None
    _cache_ttl: int = 3600  # 1 hour
    
    @staticmethod
    async def get_exchange_rates(base: str = "EUR") -> Dict[str, Decimal]:
        """
        Get current exchange rates for a base currency
        
        Returns:
            {"USD": Decimal("1.08"), "GBP": Decimal("0.85"), ...}
        """
        # Check cache
        if CurrencyConverter._cache and CurrencyConverter._cache_timestamp:
            age = (datetime.utcnow() - CurrencyConverter._cache_timestamp).seconds
            if age < CurrencyConverter._cache_ttl:
                return CurrencyConverter._cache.get(base, {})
        
        # Fetch from API
        try:
            async with httpx.AsyncClient() as client:
                if settings.EXCHANGE_RATE_API_KEY:
                    # Paid API (more reliable)
                    url = f"{settings.EXCHANGE_RATE_API_URL}{base}"
                    response = await client.get(
                        url,
                        headers={"Authorization": f"Bearer {settings.EXCHANGE_RATE_API_KEY}"},
                        timeout=10.0
                    )
                else:
                    # Free API (for development)
                    url = f"https://api.exchangerate-api.com/v4/latest/{base}"
                    response = await client.get(url, timeout=10.0)
                
                response.raise_for_status()
                data = response.json()
                
                # Convert to Decimal for precision
                rates = {
                    currency: Decimal(str(rate))
                    for currency, rate in data.get("rates", {}).items()
                }
                
                # Update cache
                CurrencyConverter._cache[base] = rates
                CurrencyConverter._cache_timestamp = datetime.utcnow()
                
                return rates
                
        except Exception as e:
            print(f"Error fetching exchange rates: {e}")
            # Return cached rates or default
            return CurrencyConverter._cache.get(base, {})
    
    @staticmethod
    async def convert(
        amount: Decimal,
        from_currency: str,
        to_currency: str
    ) -> tuple[Decimal, Decimal]:
        """
        Convert amount from one currency to another
        
        Returns:
            (converted_amount, exchange_rate)
        
        Example:
            convert(Decimal("100"), "EUR", "USD")
            # → (Decimal("108.50"), Decimal("1.085"))
        """
        # Same currency, no conversion needed
        if from_currency == to_currency:
            return amount, Decimal("1.0")
        
        # Get exchange rates
        rates = await CurrencyConverter.get_exchange_rates(from_currency)
        
        if to_currency not in rates:
            raise ValueError(f"Exchange rate not found for {to_currency}")
        
        rate = rates[to_currency]
        converted = amount * rate
        
        # Round to 2 decimals
        converted = converted.quantize(Decimal("0.01"))
        
        return converted, rate
    
    @staticmethod
    def get_currency_symbol(currency: str) -> str:
        """Get currency symbol"""
        symbols = {
            "EUR": "€",
            "USD": "$",
            "GBP": "£",
            "CHF": "CHF",
            "CAD": "CA$",
        }
        return symbols.get(currency, currency)
    
    @staticmethod
    def get_currency_name(currency: str, language: str = "en") -> str:
        """Get currency name in given language"""
        names = {
            "EUR": {"fr": "Euro", "en": "Euro", "es": "Euro", "de": "Euro"},
            "USD": {"fr": "Dollar américain", "en": "US Dollar", "es": "Dólar estadounidense", "de": "US-Dollar"},
            "GBP": {"fr": "Livre sterling", "en": "Pound Sterling", "es": "Libra esterlina", "de": "Pfund Sterling"},
            "CHF": {"fr": "Franc suisse", "en": "Swiss Franc", "es": "Franco suizo", "de": "Schweizer Franken"},
            "CAD": {"fr": "Dollar canadien", "en": "Canadian Dollar", "es": "Dólar canadiense", "de": "Kanadischer Dollar"},
        }
        return names.get(currency, {}).get(language, currency)

