from ..spot_it.utils import FloatRange
import pytest

def test_cleanup():
    float_range = FloatRange((0, 1.1), (2.3, 3), (4.1, 5.12))
    assert float_range.ranges == [(0, 1.1), (2.3, 3), (4.1, 5.12)]
    float_range = FloatRange((0, 2.5), (1, 3), (4, 5))
    assert float_range.ranges == [(0, 3), (4, 5)]
    float_range = FloatRange((0, 0.7), (0.7, 2))
    assert float_range.ranges == [(0, 2)]
    float_range = FloatRange((0, 0))
    assert float_range.ranges == [(0, 0)]

def test_random():
    float_range = FloatRange((0, 1))
    for _ in range(10):
        assert 0 <= float_range.random() <= 1
    float_range = FloatRange((0, 1), (2, 3))
    for _ in range(10):
        rand = float_range.random()
        assert 0 <= rand <= 1 or 2 <= rand <= 3
    float_range = FloatRange((100.5, 100.7))
    for _ in range(10):
        assert 100.5 <= float_range.random() <= 100.7

def test_with_buffer():
    float_range = FloatRange((0, 1))
    assert float_range.with_buffer(0.1).ranges == [(-0.1, 1.1)]
    float_range = FloatRange((0, 1), (2, 3))
    assert float_range.with_buffer(0.1).ranges == [(-0.1, 1.1), (1.9, 3.1)]
    float_range = FloatRange((100.5, 100.7))
    assert float_range.with_buffer(0.1).ranges == [(pytest.approx(100.4), pytest.approx(100.8))]
    float_range = FloatRange((0, 0.5), (0.6, 0.7))
    assert float_range.with_buffer(0.1).ranges == [(pytest.approx(-0.1), pytest.approx(0.8))]

