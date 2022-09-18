import os
import textwrap
from io import BytesIO

from fastapi import APIRouter
from PIL import Image, ImageDraw, ImageFont
from fastapi.responses import StreamingResponse


tags_metadata = ["Memes"]

balloon = APIRouter(tags=tags_metadata, prefix="/api/meme")


async def generate_image(balloon_text: str, arrow_text: str):
    cwd = os.getcwd()
    img = Image.open(f"{cwd}/assets/images/memes/balloon.bmp")

    draw = ImageDraw.Draw(img)
    font = ImageFont.truetype(f"{cwd}/assets/fonts/roboto-medium.ttf", 20)

    w, h = 300, 160
    lines = textwrap.wrap(balloon_text, width=18)
    y_text = h
    for line in lines:
        width, height = font.getsize(line)
        draw.text(
            ((w - width) / 2, y_text), line, font=font, fill="black", align="center"
        )
        y_text += height

    w, h = 250, 530
    lines = textwrap.wrap(balloon_text, width=18)
    y_text = h
    for line in lines:
        width, height = font.getsize(line)
        draw.text(
            ((w - width) / 2, y_text), line, font=font, fill="black", align="center"
        )
        y_text += height

    w, h = 1100, 520
    lines = textwrap.wrap(balloon_text, width=18)
    y_text = h
    for line in lines:
        width, height = font.getsize(line)
        draw.text(
            ((w - width) / 2, y_text), line, font=font, fill="black", align="center"
        )
        y_text += height
    draw.text((620, 185), arrow_text, "black", font)

    d = BytesIO()
    d.seek(0)
    img.save(d, "PNG")
    d.seek(0)
    return d


@balloon.get(
    "/balloon/",
    responses={200: {"content": {"image/png": {}}}},
    response_class=StreamingResponse,
)
async def generate_balloon_image(text1: str, text2: str):
    """Generates the balloon meme"""

    file = await generate_image(text1, text2)

    return StreamingResponse(file, media_type="image/png")
