import random
from hashlib import md5
from typing import Optional
from datetime import datetime, timedelta, timezone

from rich import print
from timelength import TimeLength

from core.models import Redirect, File
from core.helpers.exceptions import APIHTTPExceptions


def parse_expire_time(expire: str, max_time: Optional[int] = None) -> datetime:
    current_time = datetime.now(timezone.utc)

    if expire.isnumeric():
        return current_time + timedelta(seconds=int(expire))

    expire_time: int = TimeLength(expire).total_seconds
    if expire_time == 0:
        raise APIHTTPExceptions.INVALID_X_PROVIDED("expire time", expire)

    if max_time is not None and expire_time > max_time:
        raise APIHTTPExceptions.EXPIRE_PERIOD_TOO_LARGE()

    return current_time + timedelta(seconds=expire_time)


def generate_slug_from_seed(seed: str | bytes) -> str:
    data = seed.encode() if isinstance(seed, str) else seed
    digest = md5(data).hexdigest()
    return "".join(random.choices(digest, k=10))


async def cleanup_expired_records():
    current_time = datetime.now(timezone.utc)

    await Redirect.filter(expires_at__lt=current_time).delete()
    print("[bold red]Deleted Expired Redirect Records")

    await File.filter(expires_at__lt=current_time).delete()
    print("[bold red]Deleted Expired File Records")
