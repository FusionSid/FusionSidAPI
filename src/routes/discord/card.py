from io import BytesIO
from typing import Final, Optional

from PIL import Image
from discord import NotFound, HTTPException, Status
from fastapi.responses import RedirectResponse, StreamingResponse
from fastapi import APIRouter, Request, HTTPException as FastAPIHTTPException

from core import APIHTTPExceptions, client, get_url_image
from core.helpers import crop_image_to_circle

INVITE_URL: Final = "https://discord.gg/p9GuT5hakm"
DISCORD_SERVER_ID: Final = 942546789372952637

discord_card_endpoints = APIRouter(
    tags=["Discord Card Endpoints"], prefix="/api/discord"
)

STATUS_COLORS = {
    Status.online: "#3EA65C",
    Status.offline: "#757F8D",
    Status.idle: "#F3A51A",
    Status.dnd: "#ED4045",
    Status.do_not_disturb: "#ED4045",
    Status.invisible: "#757F8D",
    Status.streaming: "#3EA65C",
}


@discord_card_endpoints.get("/discord-server")
async def discord_server():
    return RedirectResponse(INVITE_URL)


@discord_card_endpoints.get("/pfp")
async def discord_pfp_image(
    request: Request, user_id: int, border_width: int = 5, space: Optional[int] = None
):
    if not client.is_ready():
        return FastAPIHTTPException(
            status_code=503,
            detail={
                "success": False,
                "detail": "Hol' up my guy, the bot ain't ready yet",
            },
        )

    user = await fetch_user(user_id)

    profile_picture_bytes = await get_url_image(user.display_avatar.url)

    profile_picture_buffer = BytesIO(profile_picture_bytes)
    profile_picture_buffer.seek(0)

    profile_picture_image = Image.open(profile_picture_buffer).convert("RGBA")

    cropped_pfp = crop_image_to_circle(
        profile_picture_image,
        border=True,
        border_color=STATUS_COLORS.get(user.status, STATUS_COLORS[Status.offline]),
        border_width=border_width,
        space=space,
    )

    output_image_buffer = BytesIO()
    cropped_pfp.save(output_image_buffer, "PNG")
    output_image_buffer.seek(0)

    return StreamingResponse(output_image_buffer, media_type="image/png")


async def fetch_user(user_id: int):
    guild = client.get_guild(DISCORD_SERVER_ID)
    if guild is None:
        # once fetched it will stay in cache in this code will never run
        guild = await client.fetch_guild(DISCORD_SERVER_ID)

    user = guild.get_member(user_id)
    if user is None:
        try:
            user = await guild.fetch_member(user_id)
        except (NotFound, HTTPException) as err:
            raise APIHTTPExceptions.DISCORD_USER_NOT_FOUND(user_id) from err

    return user
