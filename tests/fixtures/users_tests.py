"""Test fixtures for user tests."""
from typing import Any, Dict, List

from pytest import fixture

from contact_tracing.mock.user_tests import tests as user_tests


@fixture
def test() -> Dict[str, Any]:
    """Fixture for test.
    
    Returns:
        Dict[str, Any]: A dictionary of test.
    """
    return user_tests[0]

@fixture
def tests() -> List[Dict[str, Any]]:
    """Fixture for tests.
    
    Returns:
        List[Dict[str, Any]]: A list of tests.
    """
    return user_tests