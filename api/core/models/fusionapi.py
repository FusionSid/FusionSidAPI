""" (script)
Script to load routers and start the api  
Usage: `python3 main.py`
"""

__all__ = ["FusionSid"]

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
from slowapi.middleware import SlowAPIMiddleware
from slowapi import Limiter, _rate_limit_exceeded_handler

DESCRIPTION = """
### Made by FusionSid

[My Github](https://github.com/FusionSid)

A multipurpose API 

#### Source Code:
[https://github.com/FusionSid/FusionSidsAPI](https://github.com/FusionSid/FusionSidsAPI)

#### Contact:
Discord: FusionSid#3645
"""


class FusionSid(FastAPI):
    """
    Subclass of Fastapi for this api
    """

    def __init__(self, version: str) -> None:
        super().__init__()
        self.version = version
        self.title = "FusionSid API"
        self.description = DESCRIPTION
        self.license_info = {
            "name": "MIT",
            "url": "https://opensource.org/licenses/MIT",
        }

        # Middleware:

        # CORS
        origins = ["*"]
        self.add_middleware(
            CORSMiddleware,
            allow_origins=origins,
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )

        # Rate limiting
        self.state.limiter = Limiter(
            key_func=get_remote_address,
            default_limits=[
                "30/minute"
            ],  # set default rate limit to 30 requests per minute
        )
        self.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)
        self.add_middleware(SlowAPIMiddleware)
