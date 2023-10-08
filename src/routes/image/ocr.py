from io import BytesIO

import pytesseract
from PIL import Image
from fastapi import APIRouter, UploadFile

from core import get_url_image

ocr_endpoints = APIRouter(tags=["Image"], prefix="/api/image")


@ocr_endpoints.get("/ocr/")
async def image_ocr_url(image_url: str):
    """Uses Optical Character Recognition (OCR) to take an image and return the text inside it"""

    image_provided_buffer = BytesIO(await get_url_image(image_url))
    _image = Image.open(image_provided_buffer)

    return pytesseract.image_to_string(_image)


@ocr_endpoints.post("/ocr/")
async def image_ocr(image: UploadFile):
    """Uses Optical Character Recognition (OCR) to take an image and return the text inside it"""

    image_provided_buffer = BytesIO(await image.read())
    _image = Image.open(image_provided_buffer)

    return pytesseract.image_to_string(_image)
