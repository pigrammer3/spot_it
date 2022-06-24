"""Utilities for the Spot It application."""
import cmath
import random


def get_random_pos(
    within_radius: int, this_radius: int, plane_center: tuple[int, int]
) -> tuple[int, int]:
    """
    Get a random position for the upper left of a circle with radius `this_radius` within a circle
    with radius `within_radius`.
    """
    radius = random.randrange(within_radius - this_radius - 20)
    theta = random.randrange(360)
    complex_center = cmath.rect(radius, theta)
    center = (
        int(complex_center.real) + plane_center[0],
        int(complex_center.imag) + plane_center[1],
    )
    return (center[0] - this_radius, center[1] - this_radius)
