"""Tests for date functions."""
from typing import Tuple

import pytest
from dateutil import parser

from contact_tracing.common.date import difference_in_days


@pytest.mark.parametrize(
    ("input_data", "expected"),
    [(("2020-01-01T00:00:00Z", "2020-01-01T00:00:00Z"), 0), (("2020-01-01T00:00:00Z", "2020-01-01T16:00:00Z"), 0)],
)
def test_same_day(input_data: Tuple[str, str], expected: int) -> None:
    """Parametrized test to check if the difference between the same dates is 0.

    Args:
        input_data (Tuple[str, str]): Pair of dates to calculate the difference between.
        expected (int): The expected difference between the dates in days.
    """
    to_date = parser.parse(input_data[0])
    from_date = parser.parse(input_data[1])

    actual = difference_in_days(to_date, from_date)
    assert actual == expected, "If both the dates are the same, then the difference must be 0"


@pytest.mark.parametrize(
    ("input_data", "expected"),
    [
        (("2020-01-01T00:00:00Z", "2020-01-02T00:00:00Z"), 1),
        (("2020-01-01T00:00:00Z", "2020-01-02T23:00:00Z"), 1),
        (("2020-01-01T00:00:00Z", "2020-01-10T00:00:00Z"), 9),
        (("2020-01-01T00:00:00Z", "2020-02-01T00:00:00Z"), 31),
    ],
)
def test_difference(input_data: Tuple[str, str], expected: int) -> None:
    """Parameterized test for the difference between two dates function.

    Each input_data value is iterated and checked against the expected value.

    Args:
        input_data (Tuple[str, str]): Pair of dates to calculate the difference between.
        expected (int): The expected difference between the dates in days.
    """
    from_date = parser.parse(input_data[0])
    to_date = parser.parse(input_data[1])

    actual = difference_in_days(from_date, to_date)
    assert (
        actual == expected
    ), f"If the dates are {input_data[0]} and {input_data[1]}, then the difference must be {expected}"


@pytest.mark.parametrize(
    ("input_data", "expected"),
    [
        (("2020-01-02T00:00:00Z", "2020-01-01T00:00:00Z"), -1),
        (("2020-01-10T00:00:00Z", "2020-01-01T00:00:00Z"), -9),
        (("2020-02-01T00:00:00Z", "2020-01-01T00:00:00Z"), -31),
    ],
)
def test_negative_difference(input_data: Tuple[str, str], expected: int) -> None:
    """Parameterized test for the difference between two dates function for negative values.

    Each input_data value is iterated and checked against the expected value.

    Args:
        input_data (Tuple[str, str]): Pair of dates to calculate the difference between.
        expected (int): The expected difference between the dates in days.
    """
    from_date = parser.parse(input_data[0])
    to_date = parser.parse(input_data[1])

    actual = difference_in_days(from_date, to_date)
    assert actual == expected, f"If the dates are {from_date} and {to_date}, then the difference must be {expected}"
