from fastapi import APIRouter

from core.utils import create_bedwars_image

hypixel_stat_endpoints = APIRouter(tags=["Minecraft"], prefix="/api/minecraft")


@hypixel_stat_endpoints.get("/bwstats")
async def show_bedwars_stats(player: str):
    images = await create_bedwars_image(player)
    return images
