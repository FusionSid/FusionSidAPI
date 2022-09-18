from slowapi import Limiter
from pydantic import BaseModel
from fastapi import APIRouter, Request
from slowapi.util import get_remote_address

from core.utils import run_code

limiter = Limiter(key_func=get_remote_address)


class Code(BaseModel):
    code: str
    language: str


tags_metadata = ["Run code in a language"]
runcode_endpoints = APIRouter(tags=tags_metadata, prefix="/api")


@runcode_endpoints.post("/runcode")
@limiter.limit("10/minute")
async def run_the_code(request: Request, code: Code):
    """Code Execution Engine - Run code in a language"""

    output = await run_code(code.code, language=code.language, await_task=True)
    return {"output": output}
