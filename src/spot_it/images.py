"""Image manipulation for Spot-It!"""
import math

# import random

from PIL import Image, ImageDraw

from .randomization import RandomizeImageInfo
from .utils import to_complex, to_int_tuple  # PlacedImage, get_random_pos,

CIRCLE_SCALE = 4
BACKGROUND = (255, 255, 255, 0)
CIRCLE_OUTLINE = (0, 0, 0, 255)
# RANDOM_PERCISION = 30
# CROP_PERCISION = 10


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


def make_image_random(image: Image.Image, info: RandomizeImageInfo) -> Image.Image:
    """Randomize the scale and rotation of the image, to use as a spot-it symbol."""
    dimensions = to_complex(image.size)
    # Multiply the radius by two so we don't have to divide the dimensions by 2
    scale = info.radius * 2 / math.hypot(dimensions.real, dimensions.imag)

    resized = image.resize(to_int_tuple(dimensions * scale))
    rotated = resized.rotate(info.rotation, expand=True, fillcolor=BACKGROUND)
    return rotated


def crop_to_minimum(image: Image.Image) -> Image.Image:
    """Crop an image to its minimum boundary box."""
    return image.crop(image.getbbox())


def spot_it_card(images: list[Image.Image], size: int) -> Image.Image:
    """Generate a Spot It! card from a list of images."""
    card = get_circle(size)
    placed_images: list[tuple[Image.Image, RandomizeImageInfo]] = []
    while len(placed_images) != len(images):
        placed_images = []
        for image in images:
            placed_info = list(map(lambda item: item[1], placed_images))
            random_info = RandomizeImageInfo(size, placed_info)
            counter = 0
            while not all(map(random_info.dont_overlap, placed_info)):
                # If we've done this ten times, it must be a difficult card. Start over.
                if counter >= 10:
                    break
                random_info = RandomizeImageInfo(size, placed_info)
                counter += 1
            else:
                placed_images.append((image, random_info))
                continue
            break
    # Wait to preform image manipulation until the end to increase performance.
    for image, info in placed_images:
        randomized = make_image_random(image, info)
        card.paste(
            randomized,
            to_int_tuple(info.center - to_complex(randomized.size) / 2),
            randomized,
        )
    return card
