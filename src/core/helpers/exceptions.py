""" (module) exception
This module contains exceptions to make development easier
"""

import sys
from enum import Enum
from typing import Any

from rich.text import Text
from rich.panel import Panel
from rich.console import Console
from fastapi import HTTPException
from PIL.ImageColor import colormap


class BaseException(Exception):
    """Base class for other exceptions to inherit form"""

    pass


class HTTPStatusCodes(Enum):
    """Custom HTTP status codes to use internally"""

    EXAMPLE_STATUS_CODE = 461


class RichBaseException(BaseException):
    """
    Base rich class for other exceptions to inherit form
    This one prints the error to console with rich
    """

    def __init__(self, title: str, message: str) -> None:
        error_message = Panel(
            Text.from_markup(f"[yellow]{message}"),
            title=title,
            border_style="red",
        )
        Console().print(error_message, justify="left")
        super().__init__()


class InvalidDevmodeValue(RichBaseException):
    def __init__(self, provided: str) -> None:
        super().__init__(
            "INVALID RUN MODE!!!",
            f"DEVMODE can either be 'true' or 'false'. You provided: {provided} which is not valid!",
        )
        sys.exit(1)


class NoAssetsDirectory(RichBaseException):
    def __init__(
        self,
    ) -> None:
        super().__init__(
            "No Assets Directory!!!",
            "Please ensure that the assets directory exists as it is required for the api to function",
        )
        sys.exit(1)


class InvalidColorProvided(HTTPException):
    def __init__(self, provided: str | int | list) -> None:
        status_code = 400
        detail = {
            "success": False,
            "detail": "The color that you provided was invalid. ",
            "provided": provided,
            "tip": "It must be either a hex color prefixed with # or one of the supported colors below",
            "supported_colors": colormap,
        }

        super().__init__(status_code, detail)


class FailedToFetchError(HTTPException):
    def __init__(self, provided: str) -> None:
        status_code = 400
        detail = {
            "success": False,
            "detail": "Could not fetch data from the url provided",
            "provided": provided,
            "tip": "URL is most likely invalid or the wrong link",
        }

        super().__init__(status_code, detail)


class InvalidXProvided(HTTPException):
    def __init__(self, thing: str, provided: Any) -> None:
        status_code = 400
        detail = {
            "success": False,
            "detail": f"The {thing} provided was not valid",
            "provided": provided,
        }

        super().__init__(status_code, detail)


class APIHTTPExceptions:
    """
    All the api's http exceptions in a class so they are all together
    """

    INVALID_COLOR_PROVIDED = InvalidColorProvided
    FAILED_TO_FETCH_ERROR = FailedToFetchError
    INVALID_X_PROVIDED = InvalidXProvided
