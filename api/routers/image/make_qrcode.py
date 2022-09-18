from io import BytesIO

import qrcode as qrc
from fastapi import APIRouter, Request
from fastapi.responses import StreamingResponse

tags_metadata = ["Image"]

qrcode_endpoints = APIRouter(tags=tags_metadata, prefix="/api/image")


async def make_qrcode(url):
    qr = qrc.QRCode(
        version=1,
        error_correction=qrc.constants.ERROR_CORRECT_H,
        box_size=10,
        border=4,
    )
    qr.add_data(str(url))
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white").convert("RGB")
    d = BytesIO()
    d.seek(0)
    img.save(d, "PNG")
    d.seek(0)
    return d


@qrcode_endpoints.get("/qrcode")
async def generate_qrcode(link: str):
    """Create a qr code"""

    file = await make_qrcode(link)
    return StreamingResponse(file, media_type="image/png")
