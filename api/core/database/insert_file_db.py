import os
import time
import string
import random
import asyncio

import aiosqlite
from dotenv import load_dotenv


load_dotenv()
DB_PATH = os.environ["MAIN_DB"] + "/main.db"


async def get_file(code):
    async with aiosqlite.connect(DB_PATH) as db:
        cur = await db.execute("SELECT * FROM Files WHERE file_code=?", (code,))
        data = await cur.fetchall()
    try:
        return data[0]
    except IndexError:
        return False


async def check_code_exists(code: str):
    async with aiosqlite.connect(DB_PATH) as db:
        cur = await db.execute(f"SELECT * FROM Files WHERE file_code=?", (code,))
        data = await cur.fetchall()

    if len(data) == 0:
        return True

    return False


async def generate_code(custom_code: str = None):
    if custom_code is not None:
        does_code_exist = await check_code_exists(custom_code)
        if does_code_exist:
            return custom_code

    choices = string.ascii_lowercase + string.ascii_uppercase + string.digits
    while True:
        code = "".join(random.sample(choices, 8))
        does_code_exist = await check_code_exists(code)
        if does_code_exist:
            break

    return code


async def insert_file(file_data: bytes, file_type: str, custom_code: str = None):
    time_right_now = int(time.time())
    code = await generate_code(custom_code=custom_code)

    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute(
            "INSERT INTO Files (time_added, file_code, file_type, file_data) VALUES (?, ?, ?, ?)",
            (
                time_right_now,
                code,
                file_type,
                file_data,
            ),
        )

        await db.commit()
    return code


async def get_full_db():
    async with aiosqlite.connect(DB_PATH) as db:
        cur = await db.execute("SELECT * FROM Files")
        data = await cur.fetchall()
    return data


async def loop_temphost_cleanup():
    # Deletes all files that have been in the db for more than 24h
    delete_interval = 86_400  # seconds

    # Checks every 6 hours
    check_every = 21_600  # seconds

    while True:
        time_right_now = int(time.time())
        data = await get_full_db()
        for file in data:
            time_added = file[1]
            if (time_right_now - time_added) > delete_interval:
                async with aiosqlite.connect(DB_PATH) as db:
                    await db.execute(
                        "DELETE FROM Files WHERE file_id=? and file_code=?",
                        (
                            file[0],
                            file[2],
                        ),
                    )
                    await db.commit()
                    await db.execute("VACUUM")

        await asyncio.sleep(check_every)
