__all__ = ("client",)

import discord
from rich import print
from discord.ext import commands

intents = discord.Intents.all()
client = commands.Bot(">", intents=intents, help_command=None)


@client.event
async def on_ready():
    print("[bold blue]Bot is ready!")
