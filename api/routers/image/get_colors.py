from io import BytesIO
from fastapi import Request
from colorthief import ColorThief
from fastapi import APIRouter, UploadFile

tags_metadata = ["Image"]
get_color_endpoints = APIRouter(tags=tags_metadata, prefix="/api/image")


async def get_image_colors(image, _hex):
    color_thief = ColorThief(image)
    dominant_color = list(color_thief.get_color(quality=1))
    palette = color_thief.get_palette(color_count=6)
    palette = [list(i) for i in palette]

    if _hex:
        dominant_color = ("#{:X}{:X}{:X}").format(
            dominant_color[0], dominant_color[1], dominant_color[2]
        )

        for index, color in enumerate(palette):
            palette[index] = ("#{:X}{:X}{:X}").format(color[0], color[1], color[2])

    return {"dominant_color": dominant_color, "palette": palette}


@get_color_endpoints.post("/get_colors/")
async def find_colors(request: Request, image: UploadFile, show_hex: bool = True):
    """Gets the colors in an image"""

    img = await image.read()
    img = BytesIO(img)

    colors = await get_image_colors(img, show_hex)

    return colors
