from io import BytesIO

from colorthief import ColorThief
from fastapi import APIRouter, UploadFile

get_color_endpoints = APIRouter(tags=["Image"], prefix="/api/image")


@get_color_endpoints.post("/get_colors/")
async def find_colors(image: UploadFile, convert_to_hex: bool = True):
    """Gets the colors in an image"""

    image_provided_buffer = BytesIO(await image.read())

    color_thief = ColorThief(image_provided_buffer)

    dominant_color = list(color_thief.get_color(quality=1))
    palette: map[list[int]] = map(list, color_thief.get_palette(color_count=6))

    if not convert_to_hex:
        return {"dominant_color": dominant_color, "palette": list(palette)}

    dominant_color_hex = ("#{:X}{:X}{:X}").format(*dominant_color)
    palette_hex = [("#{:X}{:X}{:X}").format(*color) for color in palette]

    return {
        "success": True,
        "dominant_color": dominant_color_hex,
        "palette": palette_hex,
    }
