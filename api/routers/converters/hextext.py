from fastapi import APIRouter, Request

tags_metadata = ["Hex Converters"]
hex_converting_endpoints = APIRouter(tags=tags_metadata, prefix="/api/convert")


@hex_converting_endpoints.get("/text-to-hex")
async def text_to_hex(request: Request, text: str):
    """Converts text to hex"""

    output = " ".join("{:02x}".format(ord(c)) for c in text)
    return {"success": True, "hex": output}


@hex_converting_endpoints.get("/hex-to-text")
async def hex_to_text(request: Request, hex: str):
    """Converts hex text back to text"""

    output = bytearray.fromhex(hex).decode()
    return {"success": True, "text": output}
