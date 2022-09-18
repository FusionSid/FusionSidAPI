import os

from fastapi.responses import StreamingResponse
from fastapi import APIRouter, HTTPException, Request

from core.utils import font_convert


tags_metadata = ["Font Converters"]
fontconvert_endpoint = APIRouter(tags=tags_metadata, prefix="/api/font")


@fontconvert_endpoint.get("/list")
async def list_fonts(request: Request):
    """A list of the 1969 fonts you can choose from"""

    files = os.listdir("assets/fonts/")
    files = [file[:-4] for file in files]

    return {"success": True, "font_list": files}


@fontconvert_endpoint.get("/convert")
async def convert_text_to_font(
    request: Request,
    text: str,
    font: str,
    text_color: str = "black",
):
    """Converts text to any font you want, They are 1969 fonts to choose from"""
    image = await font_convert(text, font, 0, text_color)
    if image is None:
        raise HTTPException(
            status_code=403,
            detail="font not found, go to /api/fontconvert/list to get a list of them",
        )

    return StreamingResponse(image, media_type="image/png")
