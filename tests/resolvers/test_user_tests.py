"""Tests for user tests resolvers."""
from datetime import datetime, timezone
from typing import Dict, List, Union

import pytest
from dateutil import parser
from pytest_mock import MockerFixture

from contact_tracing.resolvers.user_test import get_test, get_tests
from contact_tracing.resolvers.user_test import to_test as test_converter
from contact_tracing.schema.user_test import TestResult


@pytest.mark.usefixtures("test")
def test_user_converter(test: Dict[str, Union[str, int]]) -> None:
    """Test for checking the JSON to User object conversion.

    Args:
        test (Dict[str, Union[str, int]]): Fixture of the test data to be converted.
    """
    parsed_test = test_converter(test)

    assert parsed_test.id == test["id"], "If parsed correctly, then the id should be the same"
    assert parsed_test.user_id == test["user_id"], "If parsed correctly, then the user_id should be the same"

    assert (
        parsed_test.test_result.name == test["test_result"]
    ), "If parsed correctly, then the test_result should be the same"
    assert parsed_test.timestamp == parser.parse(
        test["timestamp"]
    ), "If parsed correctly, then the timestamp should be the same"


@pytest.mark.usefixtures("test")
def test_get_user(test: Dict[str, Union[str, int]]) -> None:
    """Test for fetching single user.

    Args:
        test (Dict[str, Union[str, int]]): Fixture of the test data to be converted.
    """
    test_id = test["id"]
    actual_user = get_test(test_id)

    assert actual_user.id == test["id"], "If filtered correctly, then the id should be the same"
    assert actual_user.user_id == test["user_id"], "If filtered correctly, then the user_id should be the same"


@pytest.mark.usefixtures("tests")
def test_result_type_filter(tests: List[Dict[str, Union[str, int]]]) -> None:  # noqa: WPS234
    """Test for checking the filter on the test result type.

    Args:
        tests (List[Dict[str, Union[str, int]]]): Fixture of the test data to be converted.
    """
    result_type = TestResult.POSITIVE

    actual_tests = get_tests(test_result=result_type)
    expected_tests = list(filter(lambda test: test["test_result"] == result_type.name, tests))

    assert len(actual_tests) == len(
        expected_tests
    ), "If filtered correctly, then the number of tests should be the same"

    actual_ids = list(map(lambda test: test.id, actual_tests))
    expected_ids = list(map(lambda test: test["id"], expected_tests))

    assert sorted(actual_ids) == sorted(expected_ids), "If filtered correctly, then the test IDs should be the same"


@pytest.mark.usefixtures("tests")
def test_date_filter(tests: List[Dict[str, Union[str, int]]], mocker: MockerFixture) -> None:  # noqa: WPS234
    """Test for checking the filter on the test date.

    Args:
        tests (List[Dict[str, Union[str, int]]]): Fixture of the test data to be converted.
        mocker (MockerFixture): Pytest fixture for mocking.
    """
    mocked_tests = adapt_tests(tests)
    parsed_tests = list(map(test_converter, mocked_tests))
    mocker.patch("contact_tracing.resolvers.user_test.get_parsed_tests", return_value=parsed_tests)

    days = 5
    actual_tests = get_tests(days_threshold=days)

    assert len(actual_tests) == len(mocked_tests), "If filtered correctly, then the number of tests should be the same"

    actual_ids = list(map(lambda test: test.id, actual_tests))
    expected_ids = list(map(lambda test: test["id"], mocked_tests))

    assert sorted(actual_ids) == sorted(expected_ids), "If filtered correctly, then the test IDs should be the same"


def adapt_tests(tests: List[Dict[str, Union[str, int]]]) -> List[Dict[str, Union[str, int]]]:  # noqa: WPS234
    """Adapt the tests to mock the tests, especially to modify the date for testing.

    Args:
        tests (List[Dict[str, Union[str, int]]]): Fixture of the test data to be converted.

    Returns:
        List[Dict[str, Union[str, int]]]: The adapted tests.
    """
    selected_test = tests[0]
    selected_test["timestamp"] = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

    return [selected_test]
