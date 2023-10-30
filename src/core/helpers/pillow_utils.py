import numpy as np
from PIL import Image, ImageDraw


def crop_image_to_circle(image: Image.Image, border: bool = False, **kwargs):
    """
    Crop an image to be a circle and optionally add a border
    """

    np_image_array = np.array(image.convert("RGB"))

    alpha = Image.new("L", image.size, 0)

    draw = ImageDraw.Draw(alpha)
    draw.pieslice(((0, 0), image.size), 0, 360, fill=255)

    np_image_alpha = np.array(alpha)
    np_image_array = np.dstack((np_image_array, np_image_alpha))

    circle_image = Image.fromarray(np_image_array)

    if border:
        draw = ImageDraw.Draw(circle_image)
        draw.ellipse(
            (0, 0, *circle_image.size),
            outline=kwargs.get("border_color", "#000000"),
            width=kwargs.get("border_width", 5),
        )

    return circle_image
