"""Test fixtures for location."""

from typing import Any, Dict, List

from pytest import fixture

from contact_tracing.mock.users import users


@fixture
def user() -> Dict[str, Any]:
    """Fixture for user.

    Returns:
        Dict[str, Any]: A dictionary of user.
    """
    return users[0]

@fixture
def users() -> List[Dict[str, Any]]:
    """Fixture for users.

    Returns:
        List[Dict[str, Any]]: A list of users.
    """
    return users