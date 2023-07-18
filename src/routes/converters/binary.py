from fastapi import APIRouter, Request

from core import APIHTTPExceptions

binary_converting_endpoints = APIRouter(
    tags=["Binary Converters"], prefix="/api/convert"
)


@binary_converting_endpoints.get("/text-to-binary")
async def text_to_binary_endpoint(request: Request, text: str):
    """Converts text to binary"""

    result = " ".join(format(ord(x), "08b") for x in text)

    return {"success": True, "binary": result}


@binary_converting_endpoints.get("/binary-to-text")
async def binary_to_text_endpoint(request: Request, binary_text: str):
    """Converts binary to text"""

    if " " not in binary_text:
        binary_text = " ".join(
            binary_text[i : i + 8] for i in range(0, len(binary_text), 8)
        )

    try:
        result = "".join([chr(int(s, 2)) for s in binary_text.split()])
    except ValueError as err:
        raise APIHTTPExceptions.INVALID_X_PROVIDED("binary data", binary_text) from err

    return {"success": True, "text": result}
