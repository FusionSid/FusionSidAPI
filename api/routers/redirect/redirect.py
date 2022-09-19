from fastapi.responses import RedirectResponse
from fastapi import APIRouter, Request, HTTPException

from slowapi import Limiter
from slowapi.util import get_remote_address

from core.database import new_redirect_link, get_redirect

redirect_endpoints = APIRouter(tags=["URL Redirect"])
limiter = Limiter(key_func=get_remote_address)


@redirect_endpoints.post("/api/redirect/new")
# @limiter.limit("10/minute")
async def create_redirect_link(request: Request, url: str, custom_code: str = None):
    """
    Create a url redirect link.
    If you enter a custom code thats already taken it will be removed
    """
    code = await new_redirect_link(url, custom_code)
    return {
        "code": code,
        "url": f"https://api.fusionsid.xyz/r/{code}",
    }


@redirect_endpoints.get("/r/{code:str}")
async def redirect_to_link(request: Request, code: str):
    """
    Redirect to url using code
    """
    db_data = await get_redirect(code)

    if db_data == False or len(db_data) == 0:
        raise HTTPException(404, "Invalid redirect link")

    if not ("http://" in db_data[1] or "https://" in db_data[1]):
        db_data = list(db_data)
        db_data[1] = f"http://{db_data[1]}"

    return RedirectResponse(str(db_data[1]))
