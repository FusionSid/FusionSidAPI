__all__ = ("router_list", "middleware_list")

from .other import other_router
from .image import capy_endpoint

router_list = [other_router,capy_endpoint]
middleware_list = []
