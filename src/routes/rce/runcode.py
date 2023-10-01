from typing import Final, Literal

import aiohttp
from pydantic import BaseModel
from fastapi import APIRouter, Request

from core import APIHTTPExceptions

API_URL: Final = "https://rce.fusionsid.com/runcode"
LANGUAGES = Literal["python", "node", "c", "ricklang"]

runcode_endpoints = APIRouter(tags=["Code Execution Engine"], prefix="/api")


class RunCodeJob(BaseModel):
    language: LANGUAGES
    code: str
    input: str = ""
    use_cache: bool = True
    enviromentVariables: dict[str, str] = {}


@runcode_endpoints.post("/rce")
async def run_code(request: Request, data: RunCodeJob):
    """Runs arbitrary code in a language (proxy for https://rce.fusionsid.com/runcode)"""

    async with aiohttp.ClientSession() as session:
        async with session.post(API_URL, json=dict(data)) as resp:
            try:
                response = await resp.json()
            except Exception as err:
                raise APIHTTPExceptions.FAILED_TO_FETCH_ERROR(API_URL) from err

    return response
