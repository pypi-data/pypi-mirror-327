"""Exceptions for exratepy client."""

from loguru import logger


class ApiResponseError(Exception):
    """Class used to document API exceptions."""

    def __init__(self, url: str, message: str) -> None:
        """Raises an exception with URL that caused the error, the status code and the error message.

        Args:
            url (str): URL which caused the error.
            status_code (int): Status code of the response.
            message (str): Error message received as response.

        """
        self.message = f"Request to {url} failed. Response: {message}"
        logger.error(self.message)
        super().__init__(self.message)
