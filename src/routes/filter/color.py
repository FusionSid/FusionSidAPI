import itertools
from io import BytesIO
from typing import Final, Literal, Callable

from PIL import Image
from fastapi.responses import StreamingResponse
from fastapi import APIRouter, UploadFile, Query

from core import get_url_image

color_filter_endpoint = APIRouter(tags=["Image Filters"], prefix="/api/filter")

COLOR = Literal[
    "RED",
    "GREEN",
    "BLUE",
    "YELLOW",
    "PINK",
    "PURPLE",
    "GREY",
    "SEPIA",
]
COLOR_TYPE = Final[dict[COLOR, Callable[..., tuple[int, int, int]]]]
COLOR_CONVERTERS: COLOR_TYPE = {
    "RED": lambda r, g, b: (r, 0, 0),
    "GREEN": lambda r, g, b: (0, g, 0),
    "BLUE": lambda r, g, b: (0, 0, b),
    "YELLOW": lambda r, g, b: (r, g, 0),
    "PINK": lambda r, g, b: (r, 0, b),
    "PURPLE": lambda r, g, b: (r, 0, b),
    "GREY": lambda r, g, b: ((r + g + b) // 3,) * 3,
    "SEPIA": lambda r, g, b: (
        int((r * 0.396) + (g * 0.769) + (b * 0.189)),
        int((r * 0.349) + (g * 0.686) + (b * 0.168)),
        int((r * 0.272) + (g * 0.534) + (b * 0.131)),
    ),
}


def apply_color(image: Image.Image, color: COLOR) -> StreamingResponse:
    conversion_function = COLOR_CONVERTERS[color]

    (
        width,
        height,
    ) = image.size
    output_image = Image.new("RGB", (width, height))

    for height_px, width_px in itertools.product(range(height), range(width)):
        r, g, b = image.getpixel((width_px, height_px))
        output_image.putpixel((width_px, height_px), conversion_function(r, g, b))

    image_buffer = BytesIO()
    output_image.save(image_buffer, "PNG")
    image_buffer.seek(0)

    return StreamingResponse(image_buffer, media_type="image/png")


@color_filter_endpoint.get("/color")
async def apply_color_filter_to_url(
    image_url: str, color: COLOR = Query(None, enum=tuple(COLOR_CONVERTERS.keys()))
):
    """Puts a color filter on an image"""

    original_image_buffer = BytesIO(await get_url_image(image_url))
    original_image = Image.open(original_image_buffer).convert("RGB")

    return apply_color(original_image, color)


@color_filter_endpoint.post("/color")
async def apply_color_filter(
    image: UploadFile, color: COLOR = Query(None, enum=tuple(COLOR_CONVERTERS.keys()))
):
    """Puts a color filter on an image"""

    original_image_buffer = BytesIO(await image.read())
    original_image = Image.open(original_image_buffer).convert("RGB")

    return apply_color(original_image, color)
