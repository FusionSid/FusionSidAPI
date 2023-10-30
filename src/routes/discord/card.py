from io import BytesIO
from typing import Final

import numpy as np
from PIL import Image, ImageDraw
from fastapi import APIRouter, Request
from discord import NotFound, HTTPException, Status
from fastapi.responses import RedirectResponse, StreamingResponse

from core import APIHTTPExceptions, client, get_url_image

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


def create_circle(image: Image.Image):
    npImage = np.array(image.convert("RGB"))
    h, w = image.size

    alpha = Image.new("L", image.size, 0)
    draw = ImageDraw.Draw(alpha)
    draw.pieslice(((0, 0), (h, w)), 0, 360, fill=255)

    npAlpha = np.array(alpha)
    npImage = np.dstack((npImage, npAlpha))

    return Image.fromarray(npImage)


@discord_card_endpoints.get("/pfp")
async def discord_pfp_image(request: Request, user_id: int):
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

    profile_picture_bytes = await get_url_image(user.display_avatar.url)

    profile_picture_buffer = BytesIO(profile_picture_bytes)
    profile_picture_buffer.seek(0)

    profile_picture_image = Image.open(profile_picture_buffer).convert("RGBA")

    status_color = STATUS_COLORS.get(user.status, STATUS_COLORS[Status.offline])
    cropped_pfp = create_circle(profile_picture_image)

    draw = ImageDraw.Draw(cropped_pfp)
    draw.ellipse((0, 0, *cropped_pfp.size), outline=status_color, width=5)

    output_image_buffer = BytesIO()
    cropped_pfp.save(output_image_buffer, "PNG")
    output_image_buffer.seek(0)

    return StreamingResponse(output_image_buffer, media_type="image/png")


# @discord_card_endpoints.get("/card")
# async def discord_card_image(request: Request, user_id: int):
#     ...
