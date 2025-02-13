"""Pydantic models to validate API response."""

from datetime import date

from pydantic import BaseModel, field_validator


class CurrenciesResponse(BaseModel):
    """Response model for currency information.

    Converts currency code to upper case and currency names to title case.
    """

    currencies: dict[str, str]

    @field_validator("currencies")
    @classmethod
    def validate_currencies(cls, v: dict[str, str]) -> dict[str, str]:
        """Normalize currency codes and names."""
        return {key.upper(): value.title() for key, value in v.items()}


class ExchangeRatesResponse(BaseModel):
    """Response model for exchange rate information.

    Converts currency code to upper case.
    Converts inverse rate rounded to 6 decimal places.
    """

    date: date
    rates: dict[str, float]

    @field_validator("rates")
    @classmethod
    def validate_rates(cls, v: dict[str, float]) -> dict[str, float]:
        """Normalize exchange rates.

        Converts currency codes to uppercase and calculates inverse rates
        rounded to 6 decimal places.
        """
        return {key.upper(): round(1 / value, 6) for key, value in v.items()}
