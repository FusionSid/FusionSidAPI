import json
import random
import aiofiles
from os.path import join

from fastapi import APIRouter, Request

from core import ASSETS_DIRECTORY

JSON_FILES_DIRECTORY = join(ASSETS_DIRECTORY, "json/")

fun_text_endpoints = APIRouter(tags=["Fun Text Endpoints"], prefix="/api/fun")

CACHE = {
    "compliments": [],
    "dares": [],
    "facts": [],
    "truths": [],
    "roasts": [],
    "programming_jokes": [],
    "programming_excuses": [],
    "jokes": [],
    "titled_jokes": [],
    "topics": [],
    "would_you_rather": [],
    "never_have_i_ever": [],
}


async def get_data(name: str):
    if not CACHE[name]:  # if cache is empty
        path = join(join(JSON_FILES_DIRECTORY, f"{name}.json"))
        async with aiofiles.open(path) as f:
            file_content = await f.read()
            data: list = json.loads(file_content)
        # refill cache with 15 random elements
        CACHE[name] = list(map(lambda _: random.choice(data), range(15)))

    # return an item from the cache, then remove it
    return CACHE[name].pop()


@fun_text_endpoints.get("/compliment")
async def random_compliment(request: Request):
    """Gets a random compliment"""

    return {"success": True, "compliment": await get_data("compliments")}


@fun_text_endpoints.get("/dare")
async def random_dare(request: Request):
    """Gets a random dare"""

    return {"success": True, "dare": await get_data("dares")}


@fun_text_endpoints.get("/fact")
async def random_fact(request: Request):
    """Gets a random fact"""

    return {"success": True, "fact": await get_data("facts")}


@fun_text_endpoints.get("/roast")
async def random_roast(request: Request):
    """Gets a random roast"""

    return {"success": True, "roast": await get_data("roasts")}


@fun_text_endpoints.get("/truth")
async def random_truth(request: Request):
    """Gets a random truth"""

    return {"success": True, "truth": await get_data("truths")}


@fun_text_endpoints.get("/truth-or-dare")
async def random_truth_and_dare(request: Request):
    """Gets a random truth and dare with the computers choice"""

    return {
        "success": True,
        "truth": await get_data("truths"),
        "dare": await get_data("dares"),
        "computers_choice": random.choice(["truth", "dare"]),
    }


@fun_text_endpoints.get("/joke")
async def random_joke(request: Request):
    """Gets a random joke"""

    return {"success": True, "joke": await get_data("jokes")}


@fun_text_endpoints.get("/titled-joke")
async def random_titled_joke(request: Request):
    """Gets a random titled joke"""

    return {"success": True, "joke": await get_data("titled_jokes")}


@fun_text_endpoints.get("/programming-joke")
async def random_programming_joke(request: Request):
    """Gets a random titled programming joke"""

    return {"success": True, "joke": await get_data("programming_jokes")}


@fun_text_endpoints.get("/programming-excuse")
async def random_programming_excuse(request: Request):
    """Gets a random titled programming joke"""

    return {"success": True, "excuse": await get_data("programming_excuses")}


@fun_text_endpoints.get("/topic")
async def random_topic(request: Request):
    """Gets a random topic"""

    return {"success": True, "topic": await get_data("topics")}


@fun_text_endpoints.get("/never-have-i-ever")
async def random_never_have_i_ever(request: Request):
    """Gets a random never have I ever question"""

    return {"success": True, "question": await get_data("never_have_i_ever")}


@fun_text_endpoints.get("/would-you-rather")
async def random_would_you_rather(request: Request):
    """Gets a random would you rather question"""

    return {"success": True, "question": await get_data("would_you_rather")}
