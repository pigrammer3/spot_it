"""Generate projective planes."""
import math
from collections import namedtuple
from dataclasses import dataclass
from typing import Generator, Iterable, Type, Union


class ProjectivePlaneError(ValueError):
    """Exception that can be raised when there is an error with the projective plane"""


Point: Type[tuple[int, int]] = namedtuple("Point", ["x", "y"])


@dataclass
class PointAtInfinity:
    """
    Represents a point at infinity.
    Note that the number of the point represents the slope of the lines incident with it. The value
    None for self.num represents the point incident with the vertical lines. Since vertical lines
    have no slope, math.nan may have been a better choice, but type hinting cannot represent that,
    and None is close enough.
    """

    num: int | None
    order: int

    def lines(self) -> Generator[list[Union[Point, "PointAtInfinity"]], None, None]:
        """
        Generate the lines for this point at infinity in the projective plane of order `order`.
        """
        if self.num is not None:
            for offset in range(self.order):
                yield [
                    self,
                    *(
                        Point(x, (self.num * x + offset) % self.order)
                        for x in range(self.order)
                    ),
                ]
        else:
            for offset in range(self.order):
                yield [self, *(Point(offset, x) for x in range(self.order))]

    def __hash__(self) -> int:
        return hash((self.num, self.order))

def points_at_infinity(order: int) -> Iterable[PointAtInfinity]:
    """
    Generate the points at infinity in the projective plane of order `order`. Note that each point
    is represented by a number that is the slope of the lines incident with it. None represents the
    vertical lines. Vertical lines have a slope of undefined. Although math.nan may be a better
    choice to represent this, there is no way to type hint that.
    """
    return map(
        PointAtInfinity, [*range(order), None], (order for _ in range(order + 1))
    )


def all_lines(order: int) -> Generator[list[Point | PointAtInfinity], None, None]:
    """Get all lines in the projective plane of order `order`."""
    infinity_points = list(points_at_infinity(order))
    for point in infinity_points:
        yield from point.lines()
    yield list(infinity_points)


def all_points(order: int) -> Generator[Point | PointAtInfinity, None, None]:
    """Get all points in the projective plane of order `order`."""
    for i in range(order):
        for j in range(order):
            yield Point(i, j)
    yield from points_at_infinity(order)


def get_order(number: int) -> int:
    """
    Get the order of a projective plane from the number of points or lines in it.
    If the number is not a valid number of points for a projective plane, then a
    `ProjectivePlaneError` is raised.
    """
    possible_n = math.floor(math.sqrt(number - 1))
    if possible_n**2 + possible_n + 1 != number:
        raise ProjectivePlaneError(
            "The number of points/lines in a projective field needs to conform to the formula "
            f"n² + n + 1. The nearest such number is {possible_n ** 2 + possible_n + 1}."
        )
    return possible_n
