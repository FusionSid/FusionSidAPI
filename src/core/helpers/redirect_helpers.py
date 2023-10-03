import re
import random
from hashlib import md5
from datetime import datetime, timedelta, timezone

from rich import print

from core.models import Redirect
from core.helpers.exceptions import APIHTTPExceptions

EXPIRE_TIME_REGEX = r"(\d+)([mhdw])"
SECONDS_PER_UNIT = {"m": 60, "h": 3600, "d": 86400, "w": 604800}


def parse_expire_time(expire: str) -> datetime:
    current_time = datetime.now(timezone.utc)

    if expire.isnumeric():
        return current_time + timedelta(seconds=int(expire))

    parsed = re.match(EXPIRE_TIME_REGEX, expire)
    if not parsed:
        raise APIHTTPExceptions.INVALID_X_PROVIDED("expire time", expire)

    try:
        expire_time, suffix = parsed.groups()
        seconds_delta = int(expire_time) * SECONDS_PER_UNIT[suffix]
    except (ValueError, KeyError) as err:
        raise APIHTTPExceptions.INVALID_X_PROVIDED("expire time", expire) from err

    return current_time + timedelta(seconds=seconds_delta)


def generate_slug_from_url(url: str) -> str:
    digest = md5(url.encode()).hexdigest()
    return "".join(random.choices(digest, k=10))


async def cleanup_expired_redirects():
    current_time = datetime.now(timezone.utc)
    await Redirect.filter(expires_at__lt=current_time).delete()

    print("[bold red]Deleted Expired Redirect Records")
