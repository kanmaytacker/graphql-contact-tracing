from typing import Dict, List, Tuple, Union

import pytest
from dateutil import parser

from contact_tracing.resolvers.user_location import (
    get_location,
    is_distance_valid,
    is_time_valid,
    is_user_valid,
    to_location,
)
from contact_tracing.schema.user_location import Location, UserLocation


@pytest.mark.usefixtures("location")
def test_user_converter(location: Dict[str, Union[str, int]]) -> None:
    """Test for checking the JSON to User object conversion.

    Args:
        location (Dict[str, Union[str, int]]): Fixture of the location data to be converted.
    """
    parsed_location = to_location(location)
    assert_location(parsed_location, location)


def assert_location(actual: UserLocation, expected: Dict[str, Union[str, int]]) -> None:
    """Method for asserting a location object."""
    assert actual.id == expected["id"], "If filtered correctly, then the id should be the same"
    assert actual.user_id == expected["user_id"], "If filtered correctly, then the user_id should be the same"

    assert (
        actual.location.lat == expected["location"]["lat"]
    ), "If filtered correctly, then the latitude should be the same"
    assert (
        actual.location.lng == expected["location"]["lng"]
    ), "If filtered correctly, then the longitude should be the same"
    assert actual.timestamp == parser.parse(
        expected["timestamp"]
    ), "If filtered correctly, then the timestamp should be the same"


@pytest.mark.usefixtures("location")
def test_get_location(location: Dict[str, Union[str, int]]) -> None:
    """Test for fetching single location.

    Args:
        location (Dict[str, Union[str, int]]): Fixture of the location data to be converted.
    """
    location_id = location["id"]
    actual_location = get_location(location_id)
    assert_location(actual_location, location)


@pytest.mark.parametrize(
    ("input_data", "expected"), [((1, [1, 2, 3]), True), ((1, []), False), ((1, [2, 3, 4]), False)]
)
def test_user_filtering(input_data: Tuple[int, List[int]], expected: bool) -> None:
    """Test for checking the filter on the user id.

    Args:
        input_data (Tuple[int, List[int]]): Fixture of the input data to be filtered.
        expected (bool): Expected result of the comparison.
    """
    user_id = input_data[0]
    include = input_data[1]

    actual = is_user_valid(user_id, include)

    assert actual == expected, f"If the user ID {user_id} is present in {include}, then the result should be {expected}"


@pytest.mark.parametrize(
    ("input_data", "expected"),
    [
        ((("2020-01-10T00:00:00Z", "2020-01-01T00:00:00Z"), 10), True),
        ((("2020-01-10T00:00:00Z", "2020-01-01T00:00:00Z"), 5), False),
    ],
)
def test_time_filtering(input_data: Tuple[Tuple[str, str], int], expected: bool) -> None:
    """Test for checking the filter on the time.

    Args:
        input_data (Tuple[Tuple[str, str], int]): Start and end time along with the time horizon.
        expected (bool): Expected result of the comparison.
    """
    timestamps = input_data[0]
    end_time = parser.parse(timestamps[0])
    start_time = parser.parse(timestamps[1])

    days_threshold = input_data[1]
    actual = is_time_valid(start_time, end_time, days_threshold)

    assert (
        actual == expected
    ), f"If the time is between {start_time} and {end_time}, then the result should be {expected}"


@pytest.mark.parametrize(
    ("input_data", "expected"),
    [(([(51.5007, 0.1246), (51.4995, 0.1248)], 200), True), (([(51.5007, 0.1246), (51.4995, 0.1248)], 100), False)],
)
def test_radius_filtering(input_data: Tuple[List[Tuple[float, float]], int], expected: bool) -> None:
    """Test for checking the filter on the radius.

    Args:
        input_data (Tuple[List[Tuple[float, float]], int]): List of coordinates along with the radius.
        expected (bool): Expected result of the comparison.
    """
    coordinates = input_data[0]

    start_coordinates = coordinates[0]
    start_location = Location(start_coordinates[0], start_coordinates[1])

    end_coordinates = coordinates[1]
    end_location = Location(end_coordinates[0], end_coordinates[1])

    radius = input_data[1]

    actual = is_distance_valid(start_location, end_location, radius)
    assert (
        actual == expected
    ), f"If the coordinates are {start_coordinates} and {end_coordinates} and radius is {radius}, then the result should be {expected}"
