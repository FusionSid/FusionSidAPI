import os
import json
import random
import aiofiles

from fastapi import APIRouter, Request

tags_metadata = ["Fun Text Endpoints"]
fun_text_endpoints = APIRouter(tags=tags_metadata, prefix="/api/fun")  # type: ignore


CACHE = {
    "compliment": [],
    "dare": [],
    "fact": [],
    "truth": [],
    "roast": [],
    "programming_jokes": [],
    "programming_excuses": [],
    "jokes": [],
    "titled_jokes": [],
}


async def get_data(name: str):
    global CACHE  # eww global vars lmao

    if not CACHE[name]:
        path = os.path.join(
            os.path.dirname(__file__), "../../", "assets/files/", f"{name}.json"
        )
        async with aiofiles.open(path) as f:
            file_content = await f.read()
            data = json.loads(file_content)
        CACHE[name] = [random.choice(data) for _ in range(15)]

    return CACHE[name].pop()


@fun_text_endpoints.get("/compliment")
async def random_compliment(request: Request):
    """Gets a random compliment"""

    return {"compliment": await get_data("compliment")}


@fun_text_endpoints.get("/dare")
async def random_dare(request: Request):
    """Gets a random dare"""

    return {"dare": await get_data("dare")}


@fun_text_endpoints.get("/fact")
async def random_fact(request: Request):
    """Gets a random fact"""

    return {"fact": await get_data("fact")}


@fun_text_endpoints.get("/roast")
async def random_roast(request: Request):
    """Gets a random roast"""

    return {"roast": await get_data("roast")}


@fun_text_endpoints.get("/truth")
async def random_truth(request: Request):
    """Gets a random truth"""

    return {"truth": await get_data("truth")}


@fun_text_endpoints.get("/truth-and-dare")
async def random_truth_and_dare(request: Request):
    """Gets a random truth and dare with the computers choice"""

    return {
        "truth": await get_data("truth"),
        "dare": await get_data("dare"),
        "computers_choice": random.choice(["truth", "dare"]),
    }
