__all__ = ["routes"]

from .converters import (
    fun_text_converting_endpoints,
    fontconvert_endpoint,
    hex_converting_endpoints,
    binary_converting_endpoints,
)
from .discord_card import client, discord_card_endpoints
from .code_execution import runcode_endpoints
from .fun import fun_text_endpoints
from .image import get_color_endpoints, qrcode_endpoints
from .meme import meme_endpoints
from .filters import color_filter_endpoint, blur_filter_endpoint

routes = [
    fun_text_converting_endpoints,
    fontconvert_endpoint,
    hex_converting_endpoints,
    binary_converting_endpoints,
    discord_card_endpoints,
    runcode_endpoints,
    fun_text_endpoints,
    get_color_endpoints,
    qrcode_endpoints,
    color_filter_endpoint,
    blur_filter_endpoint,
] + meme_endpoints
