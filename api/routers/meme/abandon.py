import os
from io import BytesIO

from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw
from fastapi import APIRouter
from fastapi.responses import StreamingResponse

tags_metadata = ["Memes"]

abandon = APIRouter(tags=tags_metadata, prefix="/api/meme")

# Image generate function
async def generate_image(text):
    """
    This function generate an `Abandon` Meme

    Args:
        text (str) : The text to put on the meme

    Returns:
        BytesIO image
    """
    cwd = os.getcwd()

    img = Image.open(f"{cwd}/assets/images/memes/abandon.bmp")
    draw = ImageDraw.Draw(img)
    font = ImageFont.truetype(f"{cwd}/assets/fonts/roboto-medium.ttf", 20)

    draw.text((30, 460), text, fill="black", font=font, align="center")

    d = BytesIO()
    d.seek(0)
    img.save(d, "PNG")
    d.seek(0)
    return d


@abandon.get(
    "/abandon/",
    responses={200: {"content": {"image/png": {}}}},
    response_class=StreamingResponse,
)
async def generate_abandon_image(text: str):
    """Generates the abandon meme"""

    file = await generate_image(text)

    return StreamingResponse(file, media_type="image/png")
