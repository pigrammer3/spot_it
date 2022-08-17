"""Randomization for Spot-It!"""
import cmath
import math
import random
from typing import Union


class RandomizeImageInfo:
    """Information about a randomized image"""

    rotation: int
    size: int
    center: complex
    radius: float
    already_placed: list["RandomizeImageInfo"]

    def __init__(
        self, size: int, already_placed: list["RandomizeImageInfo"]
    ) -> None:
        self.size = size
        self.already_placed = already_placed
        self.rotation = random.randrange(360)
        # Pick a radius between 2/5 and 5/5 of size so that the side lengths of the image will be
        # approximately between 3/5 and 7/5 of size.
        self.radius = ((random.random() * 3 / 5) + 2 / 5) * self.size
        self.center = self.get_random_pos()

    def get_random_pos(
        self,
    ) -> complex:
        """
        Get a random position for the upper left of a circle with radius `self.radius` within a
        circle with radius `self.size * 2`.
        """
        radius = math.sqrt(random.random()) * (
            self.size * 2 - self.radius - (self.size * 2) / 10
        )
        theta = random.randrange(360)
        # Convert to rectangular coordinates and then to origin at upper left instead of
        # origin at center.
        center = cmath.rect(radius, theta) + self.size * (2 + 2j)
        return center

    def __sub__(
        self, other: Union["RandomizeImageInfo", tuple[complex, float]]
    ) -> float:
        if isinstance(other, tuple):
            # Circle represented by tuple (center, radius)
            return abs(self.center - other[0]) - self.radius - other[1]
        return abs(self.center - other.center) - self.radius - other.radius

    def dont_overlap(
        self, other: Union["RandomizeImageInfo", tuple[complex, float]]
    ) -> bool:
        """Check if two randomized images don't overlap"""
        return (self - other) >= 0

    def __repr__(self) -> str:
        return (
            f"{self.__class__.__name__}(size={self.size}, rotation={self.rotation},"
            f"radius={self.radius}, center={self.center})"
        )
