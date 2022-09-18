import json
import random

from fastapi import APIRouter, Request


tags_metadata = ["Fun Text Endpoints"]
fun_text_endpoints = APIRouter(tags=tags_metadata, prefix="/api/fun-text")


@fun_text_endpoints.get("/compliment")
async def random_compliment(request: Request):
    """Gets a random compliment"""

    with open("./assets/files/fun_test.json") as f:
        data = json.load(f)

    return {"compliment": random.choice(data["compliment"])}


@fun_text_endpoints.get("/dare")
async def random_dare(request: Request):
    """Gets a random dare"""

    with open("./assets/files/fun_test.json") as f:
        data = json.load(f)

    return {"dare": random.choice(data["dares"])}


@fun_text_endpoints.get("/fact")
async def random_fact(request: Request):
    """Gets a random fact"""

    with open("./assets/files/fun_test.json") as f:
        data = json.load(f)

    return {"fact": random.choice(data["facts"])}


@fun_text_endpoints.get("/roast")
async def random_roast(request: Request):
    """Gets a random roast"""

    with open("./assets/files/fun_test.json") as f:
        data = json.load(f)

    return {"roast": random.choice(data["roasts"])}


@fun_text_endpoints.get("/truth")
async def random_truth(request: Request):
    """Gets a random truth"""

    with open("./assets/files/fun_test.json") as f:
        data = json.load(f)

    return {"truth": random.choice(data["truth"])}


@fun_text_endpoints.get("/truth-or-dare")
async def random_truth_and_dare(request: Request):
    """Gets a random truth and dare with the computers choice"""

    with open("./assets/files/fun_test.json") as f:
        data = json.load(f)

    return {
        "truth": random.choice(data["truth"]),
        "dare": random.choice(data["dares"]),
        "computers_choice": random.choice(["truth", "dare"]),
    }
