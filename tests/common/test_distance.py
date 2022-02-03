"""Tests for distance functions."""
from typing import Tuple

import pytest

from contact_tracing.common.distance import haversine_distance
from contact_tracing.schema.user_location import Location


@pytest.mark.parametrize(("input_data", "expected"), [(((51.5007, 0.1246), (51.5007, 0.1246)), 0)])
def test_same_location(input_data: Tuple[Tuple[float, float], Tuple[float, float]], expected: int) -> None:
    """Parametrized test to check if the distance between the same locations is 0.

    Args:
        input_data (Tuple[Tuple[float], Tuple[float, float]]): Pair of locations to calculate the distance between.
        expected (int): The expected distance between the locations in meters.
    """
    from_coordinates = input_data[0]
    from_lat, from_lng = from_coordinates
    from_location = Location(lat=from_lat, lng=from_lng)

    to_coordinates = input_data[1]
    to_lat, to_lng = to_coordinates
    to_location = Location(lat=to_lat, lng=to_lng)

    actual = haversine_distance(from_location, to_location)
    assert actual == expected, "If both the locations are the same, then the distance must be 0"


@pytest.mark.parametrize(
    ("input_data", "expected"),
    [(((51.5007, 0.1246), (51.4995, 0.1248)), 134), (((51.4995, 0.1248), (51.5007, 0.1246)), 134)],
)
def test_haversine(input_data: Tuple[Tuple[float, float], Tuple[float, float]], expected: int) -> None:
    """Parameterized test for the haversine distance function.

    Args:
        input_data (Tuple[Tuple[float], Tuple[float, float]]): Pair of locations to calculate the distance between.
        expected (int): The expected distance between the locations in meters.
    """
    from_coordinates = input_data[0]
    from_location = Location(lat=from_coordinates[0], lng=from_coordinates[1])

    to_coordinates = input_data[1]
    to_location = Location(lat=to_coordinates[0], lng=to_coordinates[1])

    actual = haversine_distance(from_location, to_location)
    assert (
        pytest.approx(actual, 1.0) == expected
    ), f"If the locations are {from_coordinates} and {to_coordinates}, then the distance must be {expected}"
