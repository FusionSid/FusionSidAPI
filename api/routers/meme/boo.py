import os
import textwrap
from io import BytesIO

from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw
from fastapi import APIRouter
from fastapi.responses import StreamingResponse

tags_metadata = ["Memes"]

boo = APIRouter(tags=tags_metadata, prefix="/api/meme")


async def generate_image(text_1: str, text_2: str):
    cwd = os.getcwd()

    img = Image.open(f"{cwd}/assets/images/memes/boo.bmp")
    draw = ImageDraw.Draw(img)
    font = ImageFont.truetype(f"{cwd}/assets/fonts/roboto-medium.ttf", 15)

    w, h = 200, 42
    lines = textwrap.wrap(text_1, width=15)
    y_text = h
    for line in lines:
        width, height = font.getsize(line)
        draw.text(
            ((w - width) / 2, y_text), line, font=font, fill="black", align="center"
        )
        y_text += height

    w, h = 680, 42
    lines = textwrap.wrap(text_2, width=15)
    y_text = h
    for line in lines:
        width, height = font.getsize(line)
        draw.text(
            ((w - width) / 2, y_text), line, font=font, fill="black", align="center"
        )
        y_text += height

    d = BytesIO()
    d.seek(0)
    img.save(d, "PNG")
    d.seek(0)
    return d


@boo.get(
    "/boo/",
    responses={200: {"content": {"image/png": {}}}},
    response_class=StreamingResponse,
)
async def generate_boo_image(text_1: str, text_2: str):
    """Generates the boo meme"""

    file = await generate_image(text_1, text_2)

    return StreamingResponse(file, media_type="image/png")
