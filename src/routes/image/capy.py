import random
from os import listdir
from os.path import join

from fastapi import APIRouter
from fastapi.responses import FileResponse

from core import ASSETS_DIRECTORY

CAPY_DIRECTORY = join(ASSETS_DIRECTORY, "images/capy_images/")
CAPY_IMAGES = listdir(CAPY_DIRECTORY)

capy_endpoint = APIRouter(tags=["Image"], prefix="/api/image")

@capy_endpoint.get("/random-capy")
async def random_card():
    """Returns a random capybara image"""
    
    image_path = join(CAPY_DIRECTORY, random.choice(CAPY_IMAGES))
    return FileResponse(image_path, media_type="image/jpeg")