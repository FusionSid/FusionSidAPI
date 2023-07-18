from fastapi import APIRouter, Request

from core import APIHTTPExceptions

hex_converting_endpoints = APIRouter(tags=["Hex Converters"], prefix="/api/convert")


@hex_converting_endpoints.get("/text-to-hex")
async def text_to_hex(request: Request, text: str):
    """Converts text to hex"""

    output = " ".join("{:02x}".format(ord(c)) for c in text)
    return {"success": True, "hex": output}


@hex_converting_endpoints.get("/hex-to-text")
async def hex_to_text(request: Request, hex_text: str):
    """Converts hex text back to text"""

    try:
        output = bytearray.fromhex(hex_text).decode()
    except ValueError as err:
        raise APIHTTPExceptions.INVALID_X_PROVIDED("hex data", hex_text) from err

    return {"success": True, "text": output}
