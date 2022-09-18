import os
from io import BytesIO

from PIL import Image
from fastapi import APIRouter
from fastapi.responses import StreamingResponse

from core.utils import get_url_image

tags_metadata = ["Memes"]

brazzers = APIRouter(tags=tags_metadata, prefix="/api/meme")


async def generate_image(image_url: str):
    profile_image = await get_url_image(image_url)
    profile = BytesIO(profile_image)
    profile.seek(0)
    size = (750, 750)
    avatar = Image.open(profile).resize(size)

    cwd = os.getcwd()
    img = Image.open(f"{cwd}/assets/images/memes/brazzers.bmp").resize((285, 59))
    avatar.paste(img, (16, 675))

    d = BytesIO()
    d.seek(0)
    avatar.save(d, "PNG")
    d.seek(0)
    return d


@brazzers.get(
    "/brazzers/",
    responses={200: {"content": {"image/png": {}}}},
    response_class=StreamingResponse,
)
async def generate_brazzers_image(image_url):
    """Generates the brazzers meme"""

    file = await generate_image(image_url)

    return StreamingResponse(file, media_type="image/png")
