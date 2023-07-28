"""Utilities for the Spot It application."""
from dataclasses import dataclass
from glob import iglob
from os.path import abspath, join
from typing import Iterable, TypeVar

from PIL import Image

T = TypeVar("T")
S = TypeVar("S")


@dataclass
class PlacedImage:
    """Represents an image which has been placed."""

    center: complex
    radius: int

    def __sub__(self, other: "PlacedImage") -> float:
        return abs(self.center - other.center) - self.radius - other.radius

    def dont_overlap(self, other: "PlacedImage") -> bool:
        """Check if two placed images don't overlap"""
        return (self - other) >= 0


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
