"""Image manipulation for Spot-It!"""
import math
import random

from PIL import Image, ImageDraw

from .utils import get_random_pos

CIRCLE_SCALE = 4
BACKGROUND = (255, 255, 255, 0)
CIRCLE_OUTLINE = (0, 0, 0, 255)
RANDOM_PERCISION = 30
CROP_PERCISION = 10


def get_max_dimension(images: list[Image.Image]) -> int:
    """Get the maximum dimension among a set of images."""
    return max(
        *(image.size[0] for image in images), *(image.size[1] for image in images)
    )


def get_circle(size: int) -> Image.Image:
    """Get a circle in black for the max dimension given."""
    image = Image.new("RGBA", (CIRCLE_SCALE * size,) * 2, BACKGROUND)
    draw = ImageDraw.Draw(image)

    draw.ellipse(
        [(0, 0), (CIRCLE_SCALE * size,) * 2],
        BACKGROUND,
        CIRCLE_OUTLINE,
        math.ceil(size / 100),
    )
    return image


def randomize_image(image: Image.Image, size: int) -> Image.Image:
    """Randomize the scale and rotation of the image, to use as a spot-it symbol."""
    image_max_dimension = max(*image.size)
    scale = (
        size
        * (
            random.randint(int(3 * RANDOM_PERCISION / 5), int(7 * RANDOM_PERCISION / 5))
            / RANDOM_PERCISION
        )
    ) / image_max_dimension

    resized = image.resize((int(image.size[0] * scale), int(image.size[1] * scale)))
    rotated = resized.rotate(random.randrange(360), expand=True, fillcolor=BACKGROUND)
    return rotated


def crop_to_square(image: Image.Image) -> Image.Image:
    """
    Crop the image such that it is a square whose inscribed circle contains everything in the
    image.

    This is useful because we want to minimize extra space in the spot-it card.
    If this is impossible, return the image cropped to a square.
    """
    center = (int(image.size[0] / 2), int(image.size[1] / 2))
    image_copy = image.copy()
    circle_draw = ImageDraw.Draw(image_copy)
    for radius in range(
        CROP_PERCISION, min(*image.size) + CROP_PERCISION, CROP_PERCISION
    ):
        circle_draw.ellipse(
            [
                (center[0] - radius, center[1] - radius),
                (center[0] + radius, center[1] + radius),
            ],
            BACKGROUND,
            BACKGROUND,
            1,
        )
        if image_copy.getcolors() is not None and len(image_copy.getcolors()) == 1:
            break
    return image.crop(
        (
            center[0] - radius,
            center[1] - radius,
            center[0] + radius,
            center[1] + radius,
        )
    )


def spot_it_card(images: list[Image.Image], size: int) -> Image.Image:
    """Generate a Spot It! card from a list of images."""
    card = get_circle(size)
    reset = 0
    for image in images:
        paste = crop_to_square(randomize_image(image, size))
        diameter = paste.size[0]
        counter = 0
        while pos := get_random_pos(
            int(CIRCLE_SCALE / 2 * size),
            int(diameter / 2),
            (int(card.size[0] / 2), int(card.size[1] / 2)),
        ):
            if counter >= 10:
                counter = 0
                paste = crop_to_square(randomize_image(image, size))
                reset += 1
            if reset >= 100:
                return spot_it_card(images, size)
            cropped = card.crop((*pos, pos[0] + paste.size[0], pos[1] + paste.size[1]))
            counter += 1
            if Image.composite(cropped, cropped, paste).getbbox() is None:
                card.paste(paste, pos, paste)
                break
    return card
