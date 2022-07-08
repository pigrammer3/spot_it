"""Image manipulation for Spot-It!"""
import math
import random

from PIL import Image, ImageDraw

from .utils import get_random_pos, to_complex, to_int_tuple, PlacedImage

CIRCLE_SCALE = 4
BACKGROUND = (255, 255, 255, 0)
CIRCLE_OUTLINE = (0, 0, 0, 255)
RANDOM_PERCISION = 30
CROP_PERCISION = 10


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

    resized = image.resize(to_int_tuple(to_complex(image.size) * scale))
    rotated = resized.rotate(random.randrange(360), expand=True, fillcolor=BACKGROUND)
    return rotated


def crop_to_square(image: Image.Image) -> Image.Image:
    """
    Crop the image such that it is a square whose inscribed circle contains everything in the
    image.

    This is useful because we want to minimize extra space in the spot-it card.
    If this is impossible, return the image cropped to a square.
    """
    bbox = image.getbbox()
    upper_left = to_complex((bbox[0], bbox[1]))
    lower_right = to_complex((bbox[2], bbox[3]))
    radius = math.ceil(abs((upper_left - lower_right) / 2))
    center = (upper_left + lower_right) / 2
    return image.crop(
        (
            *to_int_tuple(center - radius * (1 + 1j)),
            *to_int_tuple(center + radius * (1 + 1j)),
        )
    )


def spot_it_card(images: list[Image.Image], size: int) -> Image.Image:
    """Generate a Spot It! card from a list of images."""
    card = get_circle(size)
    reset = 0
    placed_images: list[PlacedImage] = []
    for image in images:
        paste = crop_to_square(randomize_image(image, size))
        radius = math.ceil(paste.size[0] / 2)
        counter = 0
        while pos := get_random_pos(
            int(CIRCLE_SCALE / 2 * size),
            radius,
            to_complex(card.size) / 2,
        ):
            if counter >= 10:
                counter = 0
                paste = crop_to_square(randomize_image(image, size))
                radius = math.ceil(paste.size[0] / 2)
                reset += 1
            if reset >= 10:
                return spot_it_card(images, size)
            counter += 1
            placed = PlacedImage(pos + radius * (1 + 1j), radius)
            if all(map(placed.dont_overlap, placed_images)):
                card.paste(paste, to_int_tuple(pos), paste)
                placed_images.append(placed)
                break
    return card
