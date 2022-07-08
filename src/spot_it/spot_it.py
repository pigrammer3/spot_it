"""The main Spot It! generator module."""
from tqdm import tqdm

from . import images, projective_plane, utils

DIRECTORY = "images"
OUTPUT_DIR = "output"


def main():
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
