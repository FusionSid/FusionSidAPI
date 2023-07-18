import random
from fastapi import APIRouter, Request

fun_text_converting_endpoints = APIRouter(
    tags=["Fun Text Converters"], prefix="/api/text"
)


@fun_text_converting_endpoints.get("/stickycaps")
async def stickycaps_endpoint(request: Request, text: str):
    """Sticky caps text"""

    lst = [str.lower, str.upper]
    output = "".join(random.choice(lst)(c) for c in text)

    return {"success": True, "text": output}


@fun_text_converting_endpoints.get("/leetspeak")
async def leetspeak_endpoint(request: Request, text: str):
    """
    Convert the English string in message and return leetspeak.
    """

    charMapping = {
        "a": ["4", "@", "/-\\"],
        "c": ["("],
        "d": ["|)"],
        "e": ["3"],
        "f": ["ph"],
        "h": ["]-[", "|-|"],
        "i": ["1", "!", "|"],
        "k": ["]<"],
        "o": ["0"],
        "s": ["$", "5"],
        "t": ["7", "+"],
        "u": ["|_|"],
        "v": ["\\/"],
    }

    leetspeak = ""

    for char in text:
        if char.lower() in charMapping and random.random() <= 0.70:
            possibleLeetReplacements = charMapping[char.lower()]
            leetReplacement = random.choice(possibleLeetReplacements)
            leetspeak = leetspeak + leetReplacement
            continue
        leetspeak = leetspeak + char

    return {"success": True, "text": leetspeak}


@fun_text_converting_endpoints.get("/expand")
async def expand_endpoint(request: Request, text: str, space: int = 1):
    """Expands T e x t"""

    spacing = " " * space
    output = spacing.join(text)

    return {"success": True, "text": output}
