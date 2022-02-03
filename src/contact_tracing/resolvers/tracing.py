"""Resolvers for generating the contact tracing graph."""
from typing import List

from contact_tracing.resolvers.user import get_users
from contact_tracing.resolvers.user_location import get_nearby_locations
from contact_tracing.resolvers.user_test import get_tests
from contact_tracing.schema.user import User
from contact_tracing.schema.user_location import Location
from contact_tracing.schema.user_test import TestResult


def get_possible_exposure(location: Location, radius: float, days_threshold: int) -> List[User]:
    """Get a list of users who could have possibly exposed the user at a given location.

    Args:
        location (Location): The location to check.
        radius (float): The radius to check.
        days_threshold (int): The number of days to check.

    Returns:
        List[User]: A list of users who could have possibly exposed the user at a given location.
    """
    # Find users who were positive in the past {days_threshold} days
    positive_cases = list(map(lambda test: test.user_id, get_tests(TestResult.POSITIVE, days_threshold)))

    # Find positive users who have crossed current location with in radius in the last {days_threshold} days
    candidates = get_nearby_locations(location, radius, days_threshold, positive_cases)
    if not len(candidates):
        return []

    # Find unique set of users that could have been a source of exposure
    user_ids = set(map(lambda candidate: candidate.user_id, candidates))

    return get_users(user_ids)
