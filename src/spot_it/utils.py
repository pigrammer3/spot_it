"""Utilities for the Spot It application."""
import cmath
import random
from glob import iglob
from os.path import abspath, join
from typing import Iterable, TypeVar

from PIL import Image

T = TypeVar("T")
S = TypeVar("S")


def get_random_pos(
    within_radius: int, this_radius: int, plane_center: complex
) -> complex:
    """
    Get a random position for the upper left of a circle with radius `this_radius` within a circle
    with radius `within_radius`.
    """
    radius = random.randrange(within_radius - this_radius - 20)
    theta = random.randrange(360)
    center = cmath.rect(radius, theta) + plane_center
    return center - radius * (1 + 1j)


def create_mapping(seq1: Iterable[T], seq2: Iterable[S]) -> dict[T, S]:
    """Create a mapping between to sequences of possibly different types."""
    return dict(zip(seq1, seq2))


def get_images(directory: str) -> list[Image.Image]:
    """
    Return a list of all PNGs in a directory.
    """
    images = []
    directory = abspath(directory)
    for file in iglob("*.png", root_dir=directory):
        images.append(Image.open(join(directory, file)))
    return images


def to_int_tuple(complex_number: complex) -> tuple[int, int]:
    """Make the real and imaginary parts of a complex number into a tuple of integers"""
    return (int(complex_number.real), int(complex_number.imag))


def to_complex(ints: tuple[int, int]) -> complex:
    """Make a tuple of integers into a complex number"""
    return ints[0] + ints[1] * 1j
