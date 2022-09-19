import os
import aiohttp

from dotenv import load_dotenv
from fastapi import HTTPException
from PIL import Image, ImageDraw, ImageFont

load_dotenv()
api_key = os.environ["HYPIXEL"]


async def get_uuid(user):
    url = f"https://api.mojang.com/users/profiles/minecraft/{user}?"
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                uuid = await response.json()
    except Exception:
        raise HTTPException(500, "User doesn't exist")
    return uuid["id"]


async def get_hydata(uuid):
    url = f"https://api.hypixel.net/player?key={api_key}&uuid={uuid}"
    async with aiohttp.ClientSession() as session:
        response = await session.get(url)
        response = await response.json()
    return response


async def get_bedwars_stats(player: str):
    uuid = await get_uuid(str(player))
    hypixel_response = await get_hydata(uuid)

    player_data = hypixel_response["player"]
    bedwars_stats = player_data["stats"]

    # Player name
    player_name = player_data["displayname"]

    # Stats
    bw_stats = bedwars_stats["Bedwars"]

    # Player rank
    rank = None
    if "monthlyPackageRank" in player_data:
        rank = "MVP++"
    elif "newPackageRank" in player_data:
        rank = player_data["newPackageRank"]
        if "_PLUS" in rank:
            rank = rank.replace("_PLUS", "+")

    return bw_stats


async def create_bedwars_image(player: str):
    return await get_bedwars_stats(player)
