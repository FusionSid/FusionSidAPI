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
from .image import get_color_endpoints, qrcode_endpoints, ocr_endpoints, card_endpoint, capy_endpoint
from .meme import meme_endpoints
from .filters import color_filter_endpoint, blur_filter_endpoint
from .minecraft import hypixel_stat_endpoints
from .redirect import redirect_endpoints
from .cdn import temp_host_endpoints

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
    hypixel_stat_endpoints,
    redirect_endpoints,
    temp_host_endpoints,
    card_endpoint,
    capy_endpoint,
    ocr_endpoints,
] + meme_endpoints
