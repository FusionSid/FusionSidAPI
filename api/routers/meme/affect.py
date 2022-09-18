import os
from io import BytesIO

from PIL import Image
from fastapi import APIRouter
from fastapi.responses import StreamingResponse

from core.utils import get_url_image

tags_metadata = ["Memes"]

affect = APIRouter(tags=tags_metadata, prefix="/api/meme")


async def generate_image(image_url: str):
    profile_image = await get_url_image(image_url)
    profile = BytesIO(profile_image)
    profile.seek(0)
    size = (200, 170)
    avatar = Image.open(profile).resize(size)
    avatar = avatar.rotate(-1)

    cwd = os.getcwd()
    img = Image.open(f"{cwd}/assets/images/memes/affect.bmp")
    img.paste(avatar, (179, 379))

    d = BytesIO()
    d.seek(0)
    img.save(d, "PNG")
    d.seek(0)
    return d


@affect.get(
    "/affect/",
    responses={200: {"content": {"image/png": {}}}},
    response_class=StreamingResponse,
)
async def generate_affect_image(image_url: str):
    """Generates the affect meme"""

    file = await generate_image(image_url)

    return StreamingResponse(file, media_type="image/png")
