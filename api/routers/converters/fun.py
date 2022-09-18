import random
from fastapi import APIRouter, Request

from core.utils import text_to_leet_speak

tags_metadata = ["Fun Text Converters"]
fun_text_converting_endpoints = APIRouter(tags=tags_metadata, prefix="/api/text")


@fun_text_converting_endpoints.get("/stickycaps")
async def stickycaps_endpoint(request: Request, text: str):
    """Sticky caps text"""

    lst = [str.lower, str.upper]
    output = "".join(random.choice(lst)(c) for c in text)

    return {"success": True, "text": output}


@fun_text_converting_endpoints.get("/leetspeak")
async def leetspeak_endpoint(request: Request, text: str):
    output = await text_to_leet_speak(text)

    return {"success": True, "text": output}


@fun_text_converting_endpoints.get("/expand")
async def expand_endpoint(request: Request, text: str, space: int = 1):
    """Expands T e x t"""

    spacing = " " * space
    output = spacing.join(text)

    return {"success": True, "text": output}
