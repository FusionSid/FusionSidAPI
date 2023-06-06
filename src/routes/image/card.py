import random
from os import listdir
from os.path import join

from fastapi import APIRouter
from fastapi.responses import FileResponse

from core import ASSETS_DIRECTORY

CARDS_DIRECTORY = join(ASSETS_DIRECTORY, "images/cards/")
CARDS_IMAGES = listdir(CARDS_DIRECTORY)

card_endpoint = APIRouter(tags=["Image"], prefix="/api/image")

@card_endpoint.get("/random-card")
async def random_card():
    """Returns a random playing card image"""
    
    image_path = join(CARDS_DIRECTORY, random.choice(CARDS_IMAGES))
    return FileResponse(image_path, media_type="image/jpeg")