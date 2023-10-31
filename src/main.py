""" (script)
python script to start the rest api and load routes
"""

__version__ = "3.0.0"
__author__ = ["FusionSid"]
__licence__ = "MIT License"

import os
import asyncio
from typing import Final
from tortoise import Tortoise
from os.path import dirname, join, exists
from contextlib import asynccontextmanager

import uvicorn
from rich import print
from fastapi import FastAPI
from dotenv import load_dotenv
from fastapi_utils.tasks import repeat_every

from routes import router_list, middleware_list
from core.helpers.exceptions import InvalidDevmodeValue, NoBotToken
from core import FusionSidAPI, TORTOISE_CONFIG, cleanup_expired_records, client

load_dotenv()


@asynccontextmanager
async def lifespan_event(app: FastAPI):
    """
    This function will run when the api starts up / shutsdown
    """

    if discord_token is None:
        raise NoBotToken

    asyncio.create_task(client.start(discord_token))

    # add all routers
    for route in router_list:
        app.include_router(router=route)

    # add all middleware
    for middleware in middleware_list:
        app.add_middleware(middleware)

    # connect to db through tortoise orm
    await Tortoise.init(
        config=TORTOISE_CONFIG,
    )

    await cleanup_expired_records()

    print("[bold blue]API has started!")

    yield

    # Will run when the api shutsdown
    await Tortoise.close_connections()
    print("[bold blue]API has been shutdown!")


@repeat_every(seconds=3600)
async def run_cleanup_tasks():
    await cleanup_expired_records()


app: Final = FusionSidAPI(__version__, lifespan=lifespan_event)
discord_token: Final = os.getenv("BOT_TOKEN")


PORT: Final = 8443 if (port := os.getenv("PORT")) is None else int(port)
SSL_CERTFILE_PATH: Final = join(dirname(__file__), "cert.pem")
SSL_KEYFILE_PATH: Final = join(dirname(__file__), "key.pem")

# check that both certificate files exist
both_certfiles_exist = all([exists(SSL_CERTFILE_PATH), exists(SSL_KEYFILE_PATH)])

# check if to startup api in dev mode or not
devmode = os.environ.get("DEVMODE", "").lower()
if devmode not in ["true", "false"]:
    raise InvalidDevmodeValue(provided=devmode)

# set the uvicorn server options based one dev mode or not
options = (
    {"app": "main:app", "port": PORT, "reload": True}
    if devmode == "true" or not both_certfiles_exist
    else {
        "app": "main:app",
        "reload": False,
        "port": PORT,
        "access_log": False,
        "ssl_keyfile": SSL_KEYFILE_PATH,
        "ssl_certfile": SSL_CERTFILE_PATH,
    }
)


if __name__ == "__main__":
    uvicorn.run(**options)
