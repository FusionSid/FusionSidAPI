__all__ = ("router_list", "middleware_list")

from .other import other_router
from .image import (
    capy_endpoint,
    card_endpoint,
    qrcode_endpoints,
    get_color_endpoints,
    ocr_endpoints,
)
from .fun import fun_text_endpoints
from .filter import blur_filter_endpoint, color_filter_endpoint
from .converters import (
    binary_converting_endpoints,
    fun_text_converting_endpoints,
    hex_converting_endpoints,
)
from .rce import runcode_endpoints
from .redirect import redirect_endpoints
from .filehost import filehost_endpoints
from .discord import discord_card_endpoints

router_list = [
    other_router,
    capy_endpoint,
    card_endpoint,
    qrcode_endpoints,
    get_color_endpoints,
    ocr_endpoints,
    fun_text_endpoints,
    blur_filter_endpoint,
    binary_converting_endpoints,
    fun_text_converting_endpoints,
    hex_converting_endpoints,
    runcode_endpoints,
    color_filter_endpoint,
    redirect_endpoints,
    filehost_endpoints,
    discord_card_endpoints,
]

middleware_list = []
