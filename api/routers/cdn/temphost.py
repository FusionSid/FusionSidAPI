import os
from io import BytesIO

from slowapi import Limiter
from dotenv import load_dotenv
from slowapi.util import get_remote_address
from fastapi.responses import StreamingResponse
from fastapi import APIRouter, UploadFile, Request

from core.database import get_file, insert_file, get_full_db

load_dotenv()

tags_metadata = ["Temporarily host a file for 24h"]
temp_host_endpoints = APIRouter(tags=tags_metadata, prefix="/api/temphost")
limiter = Limiter(key_func=get_remote_address)


@temp_host_endpoints.post("/upload")
@limiter.limit("15/minute")
async def post_upload(
    request: Request, file: UploadFile, file_type: str, file_code: str = None
):
    """
    Lets you upload a file
    Max size 50mb

    Supported file types: png, txt, jpeg, jpg, gif, mp4, mp3, json, bmp, csv, plain, ttf, pdf, otf, svg, zip
    """
    if file_code is not None and len(file_code) > 10:
        file_code = None

    ftypes = [
        "png",
        "txt",
        "jpeg",
        "jpg",
        "gif",
        "mp4",
        "mp3",
        "json",
        "bmp",
        "csv",
        "plain",
        "ttf",
        "pdf",
        "otf",
        "svg",
        "zip",
    ]
    if file_type.lower() not in ftypes:
        return {"error": "Must include valid file type", "options": ", ".join(ftypes)}

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

    mtypes = {
        "png": "image/png",
        "txt": "text/plain",
        "jpeg": "image/jpeg",
        "jpg": "image/jpg",
        "gif": "image/gif",
        "mp4": "video/mp4",
        "mp3": "audio/mpeg",
        "json": "application/json",
        "bmp": "image/bmp",
        "csv": "text/csv",
        "plain": "text/plain",
        "ttf": "font/ttf",
        "pdf": "application/pdf",
        "otf": "font/otf",
        "svg": "image/svg+xml",
        "zip": "application/zip",
    }

    if file_type in mtypes:
        return StreamingResponse(file, media_type=mtypes[file_type])
    return {"error": "Incorrect file type"}

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