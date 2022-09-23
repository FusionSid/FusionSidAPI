import asyncio
import aiosqlite
import os
from dotenv import load_dotenv

env = input("Create .env file? ")
if env.lower() in ["y", "yes"]:
    db = input("Enter path for main db: ")
    bot_token = input("Enter bot token: ")
    hypixel_key = input("Enter hypixel api key: ")

    with open(".env", "w") as f:
        f.write("MAIN_DB = {}".format(db))
        f.write("\n")
        f.write("TOKEN = {}".format(bot_token))
        f.write("\n")
        f.write("HYPIXEL = {}".format(hypixel_key))


load_dotenv()


async def main():
    async with aiosqlite.connect(f"{os.environ['MAIN_DB']}/main.db") as db:
        await db.execute(
            """CREATE TABLE IF NOT EXISTS Redirect (
            redirect_code TEXT,
            url TEXT
            )"""
        )
        await db.execute(
            """CREATE TABLE IF NOT EXISTS Files (
            file_id INTEGER PRIMARY KEY AUTOINCREMENT,
            time_added INTEGER,
            file_code TEXT,
            file_type TEXT,
            file_data BLOB
            )"""
        )


asyncio.run(main())
