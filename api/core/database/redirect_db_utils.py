import os
import string
import random

import aiosqlite
from dotenv import load_dotenv

load_dotenv()
DB_PATH = os.environ["MAIN_DB"] + "/main.db"


async def check_code_exists(code: str):
    async with aiosqlite.connect(DB_PATH) as db:
        cur = await db.execute(f"SELECT * FROM Redirect WHERE redirect_code=?", (code,))
        data = await cur.fetchall()

    if not len(data):
        return False

    return True


async def generate_code(custom_code: str = None):
    if custom_code is not None:
        if not await check_code_exists(custom_code):
            return custom_code

    choices = string.ascii_lowercase + string.ascii_uppercase + string.digits
    while True:
        code = "".join(random.choice(choices) for i in range(8))
        if not await check_code_exists(code):
            break

    return code


async def new_redirect_link(url: str, custom_code: str = None):
    code = await generate_code(custom_code=custom_code)
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute(
            "INSERT INTO Redirect (redirect_code, url) VALUES (?, ?)",
            (
                code,
                url,
            ),
        )
        await db.commit()
    return code


async def get_redirect(code):
    async with aiosqlite.connect(DB_PATH) as db:
        cur = await db.execute("SELECT * FROM Redirect WHERE redirect_code=?", (code,))
        data = await cur.fetchall()
    try:
        return data[0]
    except IndexError:
        return False
