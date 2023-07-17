from io import BytesIO

from fastapi import APIRouter
from PIL import Image, ImageFilter
from fastapi.responses import StreamingResponse

from core import get_url_image

blur_filter_endpoint = APIRouter(tags=["Image Filters"], prefix="/api/filter")


@blur_filter_endpoint.get("/blur")
async def apply_blur_filter(image_url: str, amount: int = 5):
    """Puts a blur filter on an image"""

    original_image_buffer = BytesIO(await get_url_image(image_url))
    original_image = Image.open(original_image_buffer)

    image = original_image.filter(ImageFilter.GaussianBlur(amount))

    image_buffer = BytesIO()
    image.save(image_buffer, "PNG")
    image_buffer.seek(0)

    return StreamingResponse(image_buffer, media_type="image/png")
