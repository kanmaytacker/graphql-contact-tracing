"""Test fixtures for location."""
from typing import Any, Dict, List

from pytest import fixture

from contact_tracing.mock.user_locations import locations as user_locations


@fixture
def location() -> Dict[str, Any]:
    """Fixture for location.

    Returns:
        Dict[str, Any]: A dictionary of location.
    """
    return user_locations[0]

@fixture
def locations() -> List[Dict[str, Any]]:
    """Fixture for locations.

    Returns:
        List[Dict[str, Any]]: A list of locations.
    """
    return user_locations