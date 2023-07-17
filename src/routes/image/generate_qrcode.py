from io import BytesIO

from qrcode import QRCode
from fastapi import APIRouter
from qrcode.constants import ERROR_CORRECT_H
from fastapi.responses import StreamingResponse

from core import APIHTTPExceptions

qrcode_endpoints = APIRouter(tags=["Image"], prefix="/api/image")


@qrcode_endpoints.get("/qrcode")
async def generate_qrcode(
    link: str, fill_color: str = "black", back_color: str = "white"
):
    """Generates a QR Code image given a link"""

    qr = QRCode(
        version=1,
        error_correction=ERROR_CORRECT_H,
        box_size=10,
        border=4,
    )
    qr.add_data(link)
    qr.make(fit=True)

    try:
        image = qr.make_image(fill_color=fill_color, back_color=back_color).convert(
            "RGB"
        )
    except ValueError as err:
        raise APIHTTPExceptions.INVALID_COLOR_PROVIDED(
            [fill_color, back_color]
        ) from err

    image_buffer = BytesIO()
    image.save(image_buffer, "PNG")
    image_buffer.seek(0)

    return StreamingResponse(image_buffer, media_type="image/png")
