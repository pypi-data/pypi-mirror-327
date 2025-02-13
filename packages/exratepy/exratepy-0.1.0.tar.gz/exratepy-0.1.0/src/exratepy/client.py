"""Main class used to interact with the API."""

from dataclasses import dataclass
from datetime import date
from typing import TYPE_CHECKING, Literal

if TYPE_CHECKING:
    import requests

from exratepy.api import get_data
from exratepy.models import CurrenciesResponse, ExchangeRatesResponse


@dataclass
class Client:
    """Main class used to interact with the API."""

    def get_currencies(self) -> dict[str, str]:
        """Fetch available currencies and their names.

        Returns:
            Dictionary mapping currency codes to their full names

        """
        url = "https://cdn.jsdelivr.net/npm/@fawazahmed0/currency-api@latest/v1/currencies.min.json"
        response: requests.Response = get_data(url)
        return CurrenciesResponse(currencies=response.json()).currencies

    def get_exchange_rates(self, base: str = "INR", date: date | Literal["latest"] = "latest") -> dict[str, float]:
        """Get exchange rate from API.

        Args:
            base (str, optional): Base currency for the exchange rates.. Defaults to "INR".
            date (date | str, optional): Date for the exchange rates. Defaults to "latest".

        Returns:
            dict[str, float]: Dictionary mapping currency codes to exchange rates as on the given date.

        """
        base = base.lower()
        url = f"https://cdn.jsdelivr.net/npm/@fawazahmed0/currency-api@{date}/v1/currencies/{base}.min.json"
        fallback_url = f"https://{date}.currency-api.pages.dev/v1/currencies/{base}.json"

        response: requests.Response = get_data(url=url, fallback_url=fallback_url)

        try:
            data = response.json()
        except (KeyError, ValueError) as e:
            error_message = f"Invalid data received from API: {e}"
            raise ValueError(error_message) from e
        else:
            return ExchangeRatesResponse(date=data.get("date"), rates=data.get(base)).rates
