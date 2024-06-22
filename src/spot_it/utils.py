"""Utilities for the Spot It application."""

import functools
import random
import typing
from glob import iglob
from os.path import abspath, join
from typing import Iterable, TypeVar

from PIL import Image

T = TypeVar("T")
S = TypeVar("S")


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


class FloatRange:

    ranges: list[tuple[float, float]]

    def __init__(self, *initial_ranges: tuple[float, float]):
        self.ranges = list(initial_ranges)
        self.__cleanup()

    def __cleanup(self) -> typing.Self:
        self.ranges = sorted(self.ranges, key=lambda float_range: float_range[0])
        if not self.ranges:
            return self
        merged = [self.ranges[0]]
        for current in self.ranges[1:]:
            previous = merged[-1]
            if current[0] <= previous[1]:
                upper_bound = max(previous[1], current[1])
                merged[-1] = (previous[0], upper_bound)  # merge with the previous range
            else:
                merged.append(current)
        self.ranges = merged
        return self

    def random(self) -> float:
        total_length = sum(upper - lower for lower, upper in self.ranges)
        random_value = random.random() * total_length
        for lower, upper in self.ranges:
            random_value -= upper - lower
            if random_value <= 0:
                return upper + random_value
        return self.ranges[-1][1]

    def with_buffer(self, buffer: float) -> "FloatRange":
        return FloatRange(
            *((lower - buffer, upper + buffer) for lower, upper in self.ranges)
        )

    def __contains__(self, value: float) -> bool:
        for lower, upper in self.ranges:
            if lower <= value <= upper:
                return True
        return False

    def __add__(self, other: typing.Self | tuple) -> "FloatRange":
        if isinstance(other, tuple):
            return FloatRange(*self.ranges, other)
        return FloatRange(*self.ranges, *other.ranges)

    def __sub__(self, other: tuple[int, int] | typing.Self) -> "FloatRange":
        if isinstance(other, tuple):
            result_ranges = []
            lower, upper = other
            for cur_lower, cur_upper in self.ranges:
                if cur_lower < lower < upper < cur_upper:
                    result_ranges.append((cur_lower, lower))
                    result_ranges.append((upper, cur_upper))
                elif lower <= cur_lower < cur_upper <= upper:
                    continue
                elif cur_lower < lower <= cur_upper <= upper:
                    result_ranges.append((cur_lower, lower))
                elif lower <= cur_lower <= upper < cur_upper:
                    result_ranges.append((upper, cur_upper))
                else:
                    result_ranges.append((cur_lower, cur_upper))
            return FloatRange(*result_ranges)
        return functools.reduce(FloatRange.__sub__, other.ranges, self)

    def __or__(self, other: typing.Self | tuple) -> "FloatRange":
        return self + other

    def intersection(self, other: "FloatRange") -> "FloatRange":
        result_ranges = []
        for lower, upper in self.ranges:
            for other_lower, other_upper in other.ranges:
                if other_lower <= lower <= upper <= other_upper:
                    result_ranges.append((lower, upper))
                elif lower <= other_lower <= other_upper <= upper:
                    result_ranges.append((other_lower, other_upper))
                elif other_lower <= lower <= other_upper <= upper:
                    result_ranges.append((lower, other_upper))
                elif lower <= other_lower <= upper <= other_upper:
                    result_ranges.append((other_lower, upper))
        return FloatRange(*result_ranges)

    def __and__(self, other: "FloatRange") -> "FloatRange":
        return self.intersection(other)

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({self.ranges})"

    def __str__(self) -> str:
        return " ∪ ".join(f"[{lower}, {upper}]" for lower, upper in self.ranges)

    def __bool__(self) -> bool:
        return len(self.ranges) >= 1
