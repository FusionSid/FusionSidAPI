import os
import textwrap
from io import BytesIO

from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw
from fastapi import APIRouter
from fastapi.responses import StreamingResponse

tags_metadata = ["Memes"]
violence = APIRouter(tags=tags_metadata, prefix="/api/meme")


async def generate_image(text):
    cwd = os.getcwd()

    img = Image.open(f"{cwd}/assets/images/memes/violence.jpg")
    draw = ImageDraw.Draw(img)
    font = ImageFont.truetype(f"{cwd}/assets/fonts/roboto-medium.ttf", 20)

    w, h = 960, 5
    lines = textwrap.wrap(text, width=18)
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


@violence.get(
    "/violence/",
    responses={200: {"content": {"image/png": {}}}},
    response_class=StreamingResponse,
)
async def generate_violence_image(text: str):
    """Creates the violence meme"""
    file = await generate_image(text)

    return StreamingResponse(file, media_type="image/png")
