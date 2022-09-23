from io import BytesIO

import pytesseract
from fastapi import Request
from PIL import Image
from fastapi import APIRouter, UploadFile

tags_metadata = ["Image"]
ocr_endpoints = APIRouter(tags=tags_metadata, prefix="/api/image")

@ocr_endpoints.post("/ocr/")
async def image_ocr(request: Request, image: UploadFile):
    """
    Optical character recognition (OCR)
    Takes image and returns text found in it
    """

    img = await image.read()
    img = BytesIO(img)
    img.seek(0)
    img = Image.open(img)
    text = pytesseract.image_to_string(img)

    return text
