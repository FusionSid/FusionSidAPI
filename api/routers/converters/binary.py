from fastapi import APIRouter, Request

tags_metadata = ["Binary Converters"]
binary_converting_endpoints = APIRouter(tags=tags_metadata, prefix="/api/convert")


@binary_converting_endpoints.get("/text-to-binary")
async def text_to_binary_endpoint(request: Request, text: str):
    """Converts text to binary"""

    result = " ".join(format(ord(x), "b") for x in text)

    return {"success": True, "binary": result}


@binary_converting_endpoints.get("/binary-to-text")
async def binary_to_text_endpoint(request: Request, binary_text: str):
    """Converts binary to text"""

    result = "".join([chr(int(s, 2)) for s in binary_text.split()])

    return {"success": True, "text": result}
