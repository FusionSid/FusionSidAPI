import os
from typing import Optional
from datetime import datetime

import validators
from datetime import timezone
from fastapi import APIRouter, Request, Query
from fastapi.responses import RedirectResponse
from tortoise.exceptions import ValidationError, IntegrityError

from core import APIHTTPExceptions, Redirect, generate_slug_from_seed, parse_expire_time

devmode = os.environ.get("DEVMODE", "").lower() == "true"
BASE_URL = "http://127.0.0.1:8443" if devmode else "https://api2.fusionsid.com"

redirect_endpoints = APIRouter(tags=["URL Redirect"])


@redirect_endpoints.post("/api/redirect")
async def create_redirect_link(
    request: Request,
    url: str,
    expire: Optional[str] = None,
    slug: str | None = Query(default=None, max_length=10),
):
    """Creates a new redirect URL record"""

    if not validators.url(url):
        raise APIHTTPExceptions.INVALID_X_PROVIDED("redirect URL", url)

    if slug is None:
        slug = generate_slug_from_seed(url)

    record_data = {"slug": slug, "url": url, "views": 1, "expires_at": None}

    if expire is not None:
        expire_at = parse_expire_time(expire)
        record_data["expires_at"] = expire_at

    try:
        new_record = await Redirect.create(**record_data)
    except (ValidationError, IntegrityError):
        record_data["slug"] = generate_slug_from_seed(url)
        new_record = await Redirect.create(**record_data)

    return {
        "success": True,
        "detail": "New redirect record created successfully!",
        "url": f"{BASE_URL}/r/{new_record.slug}",
        "status_url": f"{BASE_URL}/r/{new_record.slug}/stats",
    }


@redirect_endpoints.get("/r/{slug:str}")
async def redirect_to_link(request: Request, slug: str):
    try:
        redirect_record = await Redirect.filter(slug=slug).first()
    except (ValidationError, IntegrityError) as err:
        raise APIHTTPExceptions.X_NOT_FOUND("redirect record", "slug", slug) from err

    if redirect_record is None:
        raise APIHTTPExceptions.X_NOT_FOUND("redirect record", "slug", slug)

    if redirect_record.expires_at is not None:
        current_time = datetime.now(timezone.utc)
        expired = current_time > redirect_record.expires_at
        if expired:
            await redirect_record.delete()
            return {"success": False, "detail": "redirect URL record has expired"}

    redirect_record.views += 1  # type: ignore
    await redirect_record.save()

    return RedirectResponse(redirect_record.url, status_code=302)


@redirect_endpoints.get("/r/{slug:str}/stats")
async def redirect_link_stats(request: Request, slug: str):
    try:
        redirect_record = await Redirect.filter(slug=slug).first()
    except (ValidationError, IntegrityError) as err:
        raise APIHTTPExceptions.X_NOT_FOUND("redirect record", "slug", slug) from err

    if redirect_record is None:
        raise APIHTTPExceptions.X_NOT_FOUND("redirect record", "slug", slug)

    if redirect_record.expires_at is not None:
        current_time = datetime.now(timezone.utc)
        expired = current_time > redirect_record.expires_at
        if expired:
            await redirect_record.delete()
            return {"success": False, "detail": "redirect URL record has expired"}

    return {
        "success": True,
        "full_record": redirect_record,
    }
