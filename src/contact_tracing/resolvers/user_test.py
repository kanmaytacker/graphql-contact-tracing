"""Resolver functions for the UserTest type."""
from datetime import datetime, timezone
from typing import List, Optional, Union

from dateutil import parser

from contact_tracing.common.date import difference_in_days
from contact_tracing.mock.user_tests import tests
from contact_tracing.schema.user_test import TestResult, UserTest


def get_tests(test_result: Optional[TestResult] = None, days_threshold: Optional[int] = None) -> List[UserTest]:
    """Resolver function to fetch all user tests from the database.

    TODO:
        - Currently fetches from mock data. Move to database.
        - Add pagination and offset
        - Add a generic filter rather than explicit arguments.

    Args:
        test_result (TestResult, optional): The test result to be filtered on. Defaults to None.
        days_threshold ([type], optional): The number of days to calculate the time horizon. Defaults to None.

    Returns:
        List[UserTest]: A list of user tests.
    """
    parsed_tests = get_parsed_tests()
    if not test_result and not days_threshold:
        return parsed_tests

    if test_result:
        parsed_tests = list(filter(lambda test: test.test_result == test_result, parsed_tests))

    if days_threshold:
        parsed_tests = list(
            filter(
                lambda test: difference_in_days(datetime.now(timezone.utc), test.timestamp) <= days_threshold,
                parsed_tests,
            )
        )

    return parsed_tests


def get_parsed_tests() -> List[UserTest]:
    """Parser function to fetch all user tests from the database.

    Returns:
        List[UserTest]: A list of user tests.
    """
    return list(map(to_test, tests))


def to_test(test: dict[str, Union[str, int]]) -> UserTest:
    """Converts a dictionary to a UserTest object.

    Args:
        test (dict[Union[str, int]]): The dictionary to be converted.

    Returns:
        UserTest: The converted UserTest object.
    """
    timestamp = test["timestamp"]
    parsed_timestamp = parser.parse(timestamp)

    return UserTest(
        id=test["id"],
        user_id=test["user_id"],
        test_id=test["test_id"],
        timestamp=parsed_timestamp,
        test_result=TestResult[test["test_result"]],
    )


def get_test(test_id: int) -> Optional[UserTest]:
    """Resolver function to fetch a user test from the database.

    Args:
        test_id (int): The id of the user test to be fetched.

    Returns:
        Optional[UserTest]: The user test if found, else None.
    """
    return next((test for test in get_tests() if test.id == test_id), None)
