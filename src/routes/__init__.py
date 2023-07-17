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
from .filter import blur_filter_endpoint

router_list = [
    other_router,
    capy_endpoint,
    card_endpoint,
    qrcode_endpoints,
    get_color_endpoints,
    ocr_endpoints,
    fun_text_endpoints,
    blur_filter_endpoint,
]
middleware_list = []
