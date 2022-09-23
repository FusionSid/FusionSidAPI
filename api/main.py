""" (script)
Script to load routers and start the api  
Usage: `python3 main.py`
"""

import os
import asyncio

import uvicorn
from dotenv import load_dotenv
from rich.console import Console
from fastapi.responses import RedirectResponse

from routers import routes, client
from core.models import FusionSid
from core.database import loop_temphost_cleanup
from core.utils import loop_docker_cleanup

load_dotenv()

__version__ = "2.0.0"
__author__ = ["FusionSid"]

app = FusionSid(__version__)
console = Console()


# Include all routes
for route in routes:
    app.include_router(router=route)


# On startup
@app.on_event("startup")
async def startup():
    TOKEN = os.environ["TOKEN"]
    asyncio.create_task(client.start(TOKEN))

    loop = asyncio.get_event_loop()
    loop.create_task(loop_temphost_cleanup())
    loop.create_task(loop_docker_cleanup())

    console.log("[API] Starting...")


# On shutdown
@app.on_event("shutdown")
async def shutdown():
    console.log("[API] Shutting down...")


# redirect to docs
@app.get("/", tags=["Home"])
async def home():
    return RedirectResponse("/docs")


# start api
if __name__ == "__main__":
    uvicorn.run(
        f"{os.path.basename(__file__).replace('.py', '')}:app",
        host="0.0.0.0",
        port=443,
        reload=True,
    )
