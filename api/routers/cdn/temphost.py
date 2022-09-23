import os
from io import BytesIO

from slowapi import Limiter
from dotenv import load_dotenv
from slowapi.util import get_remote_address
from fastapi.responses import StreamingResponse
from fastapi import APIRouter, UploadFile, Request, Query

from core.database import get_file, insert_file, get_full_db

load_dotenv()

tags_metadata = ["Temporarily host a file for 48h"]
temp_host_endpoints = APIRouter(tags=tags_metadata, prefix="/api/temphost")
limiter = Limiter(key_func=get_remote_address)

FILE_TYPES = {
    # image
    "png": "image/png",
    "jpg": "image/jpg",
    "jpeg": "image/jpeg",
    "gif": "image/gif",
    "webp": "image/webp",
    "bmp": "image/bmp",
    "svg": "image/svg+xml",
    # video
    "mp4": "video/mp4",
    "webm": "video/webm",
    "mpeg": "video/mpeg",
    # audio
    "mp3": "audio/mpeg",
    "aac": "audio/aac",
    "midi": "audio/midi",
    "wav": "audio/wav",
    # file
    "txt": "text/plain",
    "json": "application/json",
    "javascript": "text/javascript",
    "csv": "text/csv",
    "plain": "text/plain",
    "pdf": "application/pdf",
    "xml": "application/xml",
    # font
    "ttf": "font/ttf",
    "otf": "font/otf",
    # archive
    "zip": "application/zip",
    "7z": "application/x-7z-compressed",
    "gzip": "application/gzip",
    # other / unknown / binary
    "binary": "application/octet-stream",
    "other": "application/octet-stream",
}

# In case i forget: https://developer.mozilla.org/en-US/docs/Web/HTTP/Basics_of_HTTP/MIME_types/Common_types


@temp_host_endpoints.post("/upload")
@limiter.limit("15/minute")
async def post_upload(
    request: Request,
    file: UploadFile,
    file_type: str = Query("png", enum=tuple(FILE_TYPES.keys())),
    file_code: str = None,
):
    """
    Lets you upload a file and keep it hosted for 48 hours
    Max size 50mb

    Supported file types: {}
    """.format(
        FILE_TYPES.keys()
    )

    if file_code is not None and len(file_code) > 10:
        file_code = None

    if file_type.lower() not in FILE_TYPES:
        return {
            "error": "Must include valid file type",
            "options": ", ".join(FILE_TYPES),
        }

    file = await file.read()
    if len(file) > 50_000_000:  # in bytes
        return {"error": "File to large, Max size 50mb"}

    code = await insert_file(bytes(file), file_type, file_code)
    return {
        "code": code,
        "url": f"https://api.fusionsid.xyz/api/temphost/file?code={code}",
    }


@temp_host_endpoints.get("/file")
@limiter.limit("42/minute")
async def getfile(request: Request, code: str):
    """
    Get a file with the code
    """
    db_data = await get_file(code)

    if db_data == False or len(db_data) == 0:
        return {"error": "File not found"}

    file = BytesIO(db_data[4])
    file.seek(0)

    file_type = db_data[3].lower()

    if file_type in FILE_TYPES:
        return StreamingResponse(file, media_type=FILE_TYPES[file_type])

    return StreamingResponse(file, media_type=FILE_TYPES["other"])


@temp_host_endpoints.get("/stats")
async def stats():
    """
    Stats on file uploaded
    """
    DB_PATH = os.environ["MAIN_DB"] + "/main.db"
    db_size = os.path.getsize(DB_PATH)
    return {
        "files_uploaded": len((await get_full_db())),
        "db": f"{round((db_size / 1000000), 2)}mb",
    }
