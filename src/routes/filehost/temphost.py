import os
from io import BytesIO
from datetime import datetime

from datetime import timezone
from fastapi.responses import StreamingResponse
from fastapi import APIRouter, Request, UploadFile, Query
from tortoise.exceptions import ValidationError, IntegrityError

from core import (
    APIHTTPExceptions,
    File,
    generate_slug_from_seed,
    parse_expire_time,
    ALL_MIME_TYPES,
    MIME_TYPE,
)

devmode = os.environ.get("DEVMODE", "").lower() == "true"
BASE_URL = "http://127.0.0.1:8443" if devmode else "https://api2.fusionsid.com"

MAX_HOSTING_PERIOD_SECONDS = 604_800
MAX_FILE_SIZE_BYTES = 50_000_000

filehost_endpoints = APIRouter(tags=["Temporary File Hosting"])


@filehost_endpoints.post("/api/files")
async def create_new_file(
    request: Request,
    file: UploadFile,
    file_type: MIME_TYPE = Query("png", enum=tuple(ALL_MIME_TYPES.keys())),
    expire: str = "1 day",
    slug: str | None = Query(default=None, max_length=10),
):
    """
    Uploads a new file to be hosted for a temporary period
    Max Period: 1 week
    Max File Size: 50mb
    """

    file_contents = await file.read()
    seed = file_contents[:10]
    file_size = len(file_contents)

    if file_size > MAX_FILE_SIZE_BYTES:
        raise APIHTTPExceptions.FILE_TO_LARGE()

    if slug is None:
        slug = generate_slug_from_seed(seed)

    expire_at = parse_expire_time(expire, max_time=MAX_HOSTING_PERIOD_SECONDS)
    record_data = {
        "slug": slug,
        "data": file_contents,
        "downloads": 1,
        "media_type": file_type,
        "expires_at": expire_at,
    }

    try:
        new_record = await File.create(**record_data)
    except (ValidationError, IntegrityError):
        record_data["slug"] = generate_slug_from_seed(seed)
        new_record = await File.create(**record_data)

    return {
        "success": True,
        "detail": "File uploaded successfully!",
        "url": f"{BASE_URL}/f/{new_record.slug}",
        "status_url": f"{BASE_URL}/f/{new_record.slug}/stats",
    }


@filehost_endpoints.get("/f/{slug:str}")
async def get_file(request: Request, slug: str):
    try:
        file_record = await File.filter(slug=slug).first()
    except (ValidationError, IntegrityError) as err:
        raise APIHTTPExceptions.X_NOT_FOUND("redirect record", "slug", slug) from err

    if file_record is None:
        raise APIHTTPExceptions.X_NOT_FOUND("file record", "slug", slug)

    if file_record.expires_at is not None:
        current_time = datetime.now(timezone.utc)
        expired = current_time > file_record.expires_at
        if expired:
            await file_record.delete()
            return {"success": False, "detail": "file has expired"}

    file_record.downloads += 1  # type: ignore
    await file_record.save()

    file = BytesIO(file_record.data)
    file.seek(0)

    return StreamingResponse(file, media_type=file_record.media_type)


@filehost_endpoints.get("/f/{slug:str}/stats")
async def file_stats(request: Request, slug: str):
    try:
        file_record = await File.filter(slug=slug).first()
    except (ValidationError, IntegrityError) as err:
        raise APIHTTPExceptions.X_NOT_FOUND("redirect record", "slug", slug) from err

    if file_record is None:
        raise APIHTTPExceptions.X_NOT_FOUND("file record", "slug", slug)

    if file_record.expires_at is not None:
        current_time = datetime.now(timezone.utc)
        expired = current_time > file_record.expires_at
        if expired:
            await file_record.delete()
            return {"success": False, "detail": "file has expired"}

    return {
        "success": True,
        "slug": file_record.slug,
        "created_at": file_record.created_at,
        "expires_at": file_record.expires_at,
        "downloads": file_record.downloads,
        "media_type": file_record.media_type,
    }
