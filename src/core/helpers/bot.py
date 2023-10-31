__all__ = ("client",)

import discord
import aiohttp
from rich import print
from dateutil import parser
from discord.ext import commands

intents = discord.Intents.all()
client = commands.Bot(">", intents=intents, help_command=None)


@client.event
async def on_ready():
    print("[bold blue]Bot is ready!")


@client.slash_command(description="Provide Link To Github")
async def links(ctx: discord.ApplicationContext):
    view = LinkView(
        ("API Link", "https://api.fusionsid.com/"),
        ("Github Link", "https://github.com/FusionSid/FusionSidAPI"),
    )

    await ctx.respond(
        embed=discord.Embed(title="FusionSid API Links:", color=discord.Color.random()),
        view=view,
    )


@client.slash_command(description="Show the most recent commit to the why bot repo")
async def recent_commit(ctx: discord.ApplicationContext):
    URL = "https://api.github.com/repos/FusionSid/FusionSidAPI/commits/rewrite"

    async with aiohttp.ClientSession() as session:
        async with session.get(URL) as resp:
            if resp.ok is False:
                response = None

            try:
                response = await resp.json()
            except aiohttp.ContentTypeError:
                response = None

    if response is None:
        em = discord.Embed(
            title="An error occured while trying to get the commit",
            description=("API basically had a skill issue."),
            color=discord.Colour.red(),
        )
        return await ctx.respond(embed=em, ephemeral=True)

    em = discord.Embed(
        title="FusionSid API - Most Recent Commit",
        description=f"Commit Hash: {response.get('sha')}",
        color=discord.Color.random(),
    )

    if (commit_info := response.get("committer")) is not None:
        em.set_author(
            name=f"Author: {commit_info.get('login')}",
            icon_url=commit_info.get("avatar_url"),
        )

    if response.get("commit") is not None:
        em.add_field(
            name="Message:", value=response["commit"].get("message"), inline=False
        )

        date = parser.parse(response["commit"]["committer"].get("date"))
        date = int(date.timestamp())

        em.add_field(
            name="When:",
            value=f"<t:{date}:R> <t:{date}:f>",
            inline=False,
        )

    commit_link: str = response.get("html_url")
    view = LinkView(("Link to commit", commit_link))

    await ctx.respond(embed=em, view=view)


class LinkView(discord.ui.View):
    """
    This is a view that contains a bunch of buttons.
    """

    def __init__(self, *links: tuple[str, str]):
        super().__init__(timeout=None)

        for link in links:
            self.add_item(
                discord.ui.Button(
                    style=discord.ButtonStyle.grey,
                    label=link[0],
                    url=link[1],
                )
            )
