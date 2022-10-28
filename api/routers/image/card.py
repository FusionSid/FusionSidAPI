import os
import random
from io import BytesIO

from PIL import Image
from fastapi import APIRouter
from fastapi.responses import StreamingResponse

import __main__

tags_metadata = ["Image"]

card_endpoint = APIRouter(tags=tags_metadata, prefix="/api/image")


async def get_card():
    cards = os.listdir("assets/images/cards")
    img = Image.open("assets/images/cards/"+random.choice(cards))
    
    image = BytesIO()
    img.save(image, "JPEG")
    image.seek(0)
    return image


@card_endpoint.get("/random-card")
async def random_card():
    """Returns a random card"""

    file = await get_card()
    return StreamingResponse(file, media_type="image/png")
