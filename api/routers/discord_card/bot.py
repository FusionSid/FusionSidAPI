from datetime import datetime

import discord
from discord.ext import commands
from fastapi import APIRouter, Request
from babel.dates import format_datetime
from fastapi.responses import StreamingResponse, RedirectResponse, JSONResponse

from core.utils import Card


tags_metadata = ["Discord Card Generator"]
discord_card_endpoints = APIRouter(tags=tags_metadata, prefix="/api/discord")

intents = discord.Intents.all()
client = commands.Bot(">", intents=intents, help_command=None)


@client.event
async def on_ready():
    print("Bot is ready!")


@discord_card_endpoints.get("/image")
async def generate_discord_card(
    request: Request,
    user_id: int,
    pfp_only: bool = False,
    rounded_corners: bool = True,
    show_activity: bool = True,
    resize_width: int = 450,
    show_hypesquad: bool = True,
    name_color: str = "white",
    discriminator_color: str = "white",
    activity_color: str = "white",
    border_color: None | str = None,
    background_color: str = "#161a1d",
    show_status: bool = True,
):
    """Generates a cool discord card"""
    main_guild = client.get_guild(942546789372952637)

    try:
        user = await main_guild.fetch_member(user_id)
    except Exception as error:
        if isinstance(error, discord.errors.NotFound):
            if error.code == 10007:
                guild_2 = client.get_guild(763348615233667082)
                try:
                    user = await guild_2.fetch_member(user_id)
                    main_guild = guild_2
                except discord.errors.NotFound as error_2:
                    if error_2.code == 10007:
                        return JSONResponse(
                            content={
                                "error": f"{error}",
                                "fix": "Make sure you are in the guild: https://discord.gg/p9GuT5hakm",
                            },
                            status_code=404,
                        )

            if error.code == 10013:
                return JSONResponse(
                    content={
                        "error": f"{error}",
                        "fix": "Make sure user_id is correct",
                    },
                    status_code=404,
                )

        else:
            print(error)
            return error

    user = main_guild.get_member(user_id)

    card = Card(
        user,
        rounded_corner=rounded_corners,
        resize_length=resize_width,
        name_color=name_color,
        discriminator_color=discriminator_color,
        background_color=background_color,
        activity_color=activity_color,
        show_hypesquad=show_hypesquad,
        border_color=border_color,
        show_status=show_status,
    )
    if pfp_only:
        image = await card.square_image()
    elif user.activity is not None and show_activity is True:
        image = await card.activity_image()
    else:
        image = await card.status_image()

    now = datetime.utcnow()
    format = "EEE, dd LLL yyyy hh:mm:ss"
    timern = format_datetime(now, format, locale="en") + " GMT"
    headers = {"Cache-Control": "no-cache", "Expires": timern}
    return StreamingResponse(image, 200, media_type="image/png", headers=headers)


@discord_card_endpoints.get("/discord-server")
async def discord_server():
    return RedirectResponse("https://discord.gg/p9GuT5hakm")
