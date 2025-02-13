"""Fucntions to handle all API calls."""

import requests
from loguru import logger

from exratepy.exceptions import ApiResponseError


def make_request(url: str) -> requests.Response:
    """Make a single HTTP GET request and handle errors."""
    try:
        response = requests.get(url, timeout=30)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        raise ApiResponseError(url=url, message=str(e)) from e
    else:
        logger.debug(f"Request to {url} succeeded")
        return response


def get_data(url: str, fallback_url: str | None = None) -> requests.Response:
    """Attempt to get data from primary URL, falling back to secondary URL if provided."""
    try:
        return make_request(url)
    except ApiResponseError:
        if not fallback_url:
            raise
        logger.debug(f"Falling back to Fallback URL: {fallback_url}")
        return make_request(fallback_url)
