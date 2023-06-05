""" (module) api
This contains the API class (FastAPI subclass)
"""

from typing import Final
from os.path import dirname, join, exists

from slowapi.extension import Limiter
from fastapi.responses import JSONResponse
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
from fastapi import FastAPI, Request, Response
from slowapi.middleware import SlowAPIMiddleware
from fastapi.middleware.cors import CORSMiddleware

from core.helpers.exceptions import NoAssetsDirectory

ASSETS_DIRECTORY = join(dirname(__file__), "../../../", "assets/")
try:
    assert exists(ASSETS_DIRECTORY)
except AssertionError as error:
    raise NoAssetsDirectory from error

DEFAULT_GLOBAL_RATELIMIT: Final = "42/minute"
limiter = Limiter(  # exported
    key_func=get_remote_address,
    default_limits=[DEFAULT_GLOBAL_RATELIMIT],
)


def get_description() -> str:
    """
    Get the description for the api that will be displayed in the docs

    Returns:
        str: The api's description
    """

    path = join(ASSETS_DIRECTORY, "markdown/description.md")
    with open(path) as f:
        return f.read()


class FusionSidAPI(FastAPI):
    """
    This is a subclass of fastapi.FastAPI
    Replace "The" with what the API is for (in like one word)
    """

    def __init__(self, version: str) -> None:
        # swagger docs metadata
        super().__init__(
            title="FusionSid's REST API",
            version=version,
            description=get_description(),
            license_info={
                "name": "MIT",
                "url": "https://opensource.org/licenses/MIT",
            },
        )

        # cors support
        cors_options = {
            "allow_origins": ["*"],
            "allow_methods": ["*"],
            "allow_headers": ["*"],
            "allow_credentials": True,
        }
        self.add_middleware(CORSMiddleware, **cors_options)

        # Rate Limiting
        def rate_limit_exceeded_handler(
            request: Request, exc: RateLimitExceeded
        ) -> Response:
            response = JSONResponse(
                {
                    "success": False,
                    "detail": f"Rate limit exceeded: {exc.detail}",
                    "tip": "Slow down buddy its really not that deep",
                },
                status_code=429,
            )
            response = request.app.state.limiter._inject_headers(
                response, request.state.view_rate_limit
            )
            return response

        self.state.limiter = limiter
        self.add_middleware(SlowAPIMiddleware)
        self.add_exception_handler(RateLimitExceeded, rate_limit_exceeded_handler)
