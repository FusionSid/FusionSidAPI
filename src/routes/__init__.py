__all__ = ("router_list", "middleware_list")

from .other import other_router
from .image import capy_endpoint, card_endpoint, qrcode_endpoints

router_list = [other_router, capy_endpoint, card_endpoint, qrcode_endpoints]
middleware_list = []
