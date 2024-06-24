"""The main Spot It! generator module."""
import threading
from typing import Generator
import pathlib

from PIL import Image
from tqdm import tqdm

from . import images, projective_plane, utils

DIRECTORY = pathlib.Path("images")
OUTPUT_DIR = pathlib.Path("output")


def save_image(image: Image.Image, name: pathlib.Path):
    """Save an image to filename"""
    image.save(name)


def deck():
    """main()"""
    list_of_images = utils.get_images(DIRECTORY)
    threads: list[threading.Thread] = []
    generated_deck = deck_generator(list_of_images)
    for file in [*OUTPUT_DIR.glob("*.png"), *OUTPUT_DIR.glob("*.pdf")]:
        file.unlink()
    for num, card in enumerate(
        tqdm(generated_deck, desc="Making cards", total=len(list_of_images)), start=1
    ):
        thread = threading.Thread(target=save_image, args=(card[0], OUTPUT_DIR / f"{num}.png"))
        thread.start()
        threads.append(thread)
    for thread in tqdm(threads, desc="Saving cards", total=len(threads)):
        thread.join()


def deck_generator(
    list_of_images: list[Image.Image], resolution=1000
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
