"""GraphQL schema to be exposed by the API."""
from typing import List, Optional

import strawberry

from contact_tracing.common.config import DAYS_THRESHOLD, RADIUS_THRESHOLD
from contact_tracing.resolvers.tracing import get_possible_exposure
from contact_tracing.resolvers.user import get_user, get_users
from contact_tracing.resolvers.user_location import get_locations
from contact_tracing.resolvers.user_test import get_tests
from contact_tracing.schema.tracing import TraceInput, TraceResult
from contact_tracing.schema.user import User
from contact_tracing.schema.user_location import Location, UserLocation
from contact_tracing.schema.user_test import TestResult, UserTest


@strawberry.type
class Query:
    """GraphQL query type."""

    @strawberry.field
    def users(self) -> List[User]:
        """Fetch all users.

        Returns:
            List[User]: A list of users.
        """
        return get_users()

    @strawberry.field
    def user(
        self,
        user_id: int,
    ) -> Optional[User]:
        """Fetch a user.

        Args:
            user_id (int): The id of the user to fetch.

        Returns:
            Optional[User]: The user with the given id.
        """
        return get_user(user_id)

    @strawberry.field
    def tests(self, test_result: Optional[TestResult] = None, days_threshold: Optional[int] = None) -> List[UserTest]:
        """Fetch all tests. If filters are provided, only tests matching the filters are returned.

        Args:
            test_result (Optional[TestResult], optional): Test result to be filtered on. Defaults to None.
            days_threshold (Optional[int], optional): Number of days to be considered. Defaults to None.

        Returns:
            List[UserTest]: A list of user tests.
        """
        return get_tests(test_result, days_threshold)

    @strawberry.field
    def locations(self) -> List[UserLocation]:
        """Fetch all locations.

        Returns:
            List[UserLocation]: A list of user locations.
        """
        return get_locations()

    @strawberry.field
    def trace_result(
        self,
        trace_input: TraceInput,
    ) -> TraceResult:
        """Check if a user is exposed to the different at-risk users.

        Args:
            trace_input (TraceInput): The input to be traced.

        Returns:
            TraceResult: The result of the tracing.
        """
        radius = trace_input.radius or DAYS_THRESHOLD
        days = trace_input.days or RADIUS_THRESHOLD

        location = Location(trace_input.latitude, trace_input.longitude)
        sources = get_possible_exposure(location, radius, days)
        return TraceResult(
            is_exposed=any(sources),
            sources=sources,
        )


schema = strawberry.Schema(query=Query)
