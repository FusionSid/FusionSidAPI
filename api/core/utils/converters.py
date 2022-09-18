import os
import random
from io import BytesIO

from PIL import Image, ImageFont, ImageDraw


async def text_to_leet_speak(message: str) -> str:
    """
    Convert the English string in message and return leetspeak.
    Got this from inventwithpython.com
    """

    charMapping = {
        "a": ["4", "@", "/-\\"],
        "c": ["("],
        "d": ["|)"],
        "e": ["3"],
        "f": ["ph"],
        "h": ["]-[", "|-|"],
        "i": ["1", "!", "|"],
        "k": ["]<"],
        "o": ["0"],
        "s": ["$", "5"],
        "t": ["7", "+"],
        "u": ["|_|"],
        "v": ["\\/"],
    }

    leetspeak = ""
    for char in message:
        if char.lower() in charMapping and random.random() <= 0.70:
            possibleLeetReplacements = charMapping[char.lower()]
            leetReplacement = random.choice(possibleLeetReplacements)
            leetspeak = leetspeak + leetReplacement
        else:
            leetspeak = leetspeak + char

    return leetspeak


async def font_convert(text: str, font_name: str, max_line_width: int, color: str):
    fonts_dict = {}
    for i in os.listdir("assets/fonts/"):
        fonts_dict[i[:-4]] = i
        print(i)

    try:
        the_font = fonts_dict[font_name]
    except KeyError:
        return None

    file_name = f"{os.getcwd()}/assets/fonts/{the_font}"

    font = ImageFont.truetype(file_name, 50)

    a, d = font.getmetrics()

    height = (font.getmask(text).getbbox()[3] + d) + 2
    width = (font.getmask(text).getbbox()[2]) + 2

    size = (width, height)

    image = Image.new("RGBA", size, color=(255, 255, 255, 0))
    draw = ImageDraw.Draw(image)

    try:
        draw.text((1, 1), text, fill=color, font=font)
    except ValueError:
        draw.text((1, 1), text, fill="black", font=font)

    d = BytesIO()
    d.seek(0)
    image.save(d, "PNG")
    d.seek(0)
    return d
