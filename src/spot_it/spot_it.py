"""The main Spot It! generator module."""
from typing import Generator

from PIL import Image
from tqdm import tqdm

from . import images, projective_plane, utils

DIRECTORY = "images"
OUTPUT_DIR = "output"


def deck():
    """main()"""
    list_of_images = utils.get_images(DIRECTORY)
    order = projective_plane.get_order(len(list_of_images))
    mapping = utils.create_mapping(projective_plane.all_points(order), list_of_images)
    lines = projective_plane.all_lines(order)
    for num, line in enumerate(
        tqdm(lines, desc="Making card", total=len(list_of_images)), start=1
    ):
        line_images = list(map(mapping.get, line))
        card = images.spot_it_card(line_images, 500)
        card.save(f"{OUTPUT_DIR}/{num}.png")


def deck_generator(
    list_of_images: list[Image.Image], resolution=500
) -> Generator[tuple[Image.Image, list[Image.Image]], None, None]:
    """
    Generate deck using a generator, no file IO.
    Generated values are tuples: (card, images in card).
    """
    order = projective_plane.get_order(len(list_of_images))
    mapping = utils.create_mapping(projective_plane.all_points(order), list_of_images)
    lines = projective_plane.all_lines(order)
    for line in lines:
        line_images = list(map(mapping.get, line))
        card = images.spot_it_card(line_images, resolution)
        yield (card, line_images)
