import os
from io import BytesIO

from PIL import Image
from fastapi import APIRouter
from fastapi.responses import StreamingResponse

from core.utils import get_url_image

tags_metadata = ["Memes"]
trash = APIRouter(tags=tags_metadata, prefix="/api/meme")


async def generate_image(image_url: str):
    profile_image = await get_url_image(image_url)
    profile = BytesIO(profile_image)
    profile.seek(0)
    size = (480, 485)
    avatar = Image.open(profile).resize(size)

    cwd = os.getcwd()
    img = Image.open(f"{cwd}/assets/images/memes/trash.bmp")
    img.paste(avatar, (480, 0))

    d = BytesIO()
    d.seek(0)
    img.save(d, "PNG")
    d.seek(0)
    return d


@trash.get(
    "/trash/",
    responses={200: {"content": {"image/png": {}}}},
    response_class=StreamingResponse,
)
async def generate_trash_image(image_url: str):
    """Generates the trash meme"""

    file = await generate_image(image_url)

    return StreamingResponse(file, media_type="image/png")
