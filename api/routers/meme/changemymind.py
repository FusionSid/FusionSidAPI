import os
import textwrap
from io import BytesIO

from fastapi import APIRouter
from PIL import Image, ImageDraw, ImageFont
from fastapi.responses import StreamingResponse

from core.utils import get_url_image

tags_metadata = ["Memes"]

changemymind = APIRouter(tags=tags_metadata, prefix="/api/meme")


async def generate_image(text: str):
    cwd = os.getcwd()
    img = Image.open(f"{cwd}/assets/images/memes/changemymind.bmp").convert("RGBA")
    font = ImageFont.truetype(f"{cwd}/assets/fonts/roboto-medium.ttf", 20)

    text_layer = Image.new("RGBA", size=(768, 568))
    draw = ImageDraw.Draw(text_layer)

    w, h = 900, 300
    lines = textwrap.wrap(text, width=25)
    y_text = h
    for line in lines:
        width, height = font.getsize(line)
        draw.text(
            ((w - width) / 2, y_text), line, font=font, fill="black", align="center"
        )
        y_text += height

    text_layer = text_layer.rotate(22)
    img.alpha_composite(text_layer, (0, 0))

    d = BytesIO()
    d.seek(0)
    img.save(d, "PNG")
    d.seek(0)
    return d


@changemymind.get(
    "/changemymind/",
    responses={200: {"content": {"image/png": {}}}},
    response_class=StreamingResponse,
)
async def generate_changemymind_image(text: str):
    """Generates the changemymind meme"""

    file = await generate_image(text)

    return StreamingResponse(file, media_type="image/png")
