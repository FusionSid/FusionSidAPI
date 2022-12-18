import os
import random
from io import BytesIO

from PIL import Image
from fastapi import APIRouter
from fastapi.responses import StreamingResponse

import __main__

tags_metadata = ["Image"]

capy_endpoint = APIRouter(tags=tags_metadata, prefix="/api/image")


async def get_capy():
    capys = os.listdir("assets/images/capy_images")
    img = Image.open("assets/images/capy_images/" + random.choice(capys))

    image = BytesIO()
    img.save(image, "JPEG")
    image.seek(0)
    return image


@capy_endpoint.get("/random-capy")
async def random_card():
    """Returns a random capybara image"""

    file = await get_capy()
    return StreamingResponse(file, media_type="image/jpeg")
