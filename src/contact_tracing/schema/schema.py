from typing import List, Optional

import strawberry

from contact_tracing.resolvers.tracing import get_possible_exposure
from contact_tracing.resolvers.user import get_user, get_users
from contact_tracing.resolvers.user_location import get_locations
from contact_tracing.resolvers.user_test import get_tests

from .tracing import TraceInput, TraceResult
from .user import User
from .user_location import Location, UserLocation
from .user_test import TestResult, UserTest
from contact_tracing.common.config import DAYS_THRESHOLD, RADIUS_THRESHOLD


@strawberry.type
class Query:
    @strawberry.field
    def users(self) -> List[User]:
        return get_users()

    @strawberry.field
    def user(
        self,
        id: int,
    ) -> Optional[User]:
        return get_user(id)

    @strawberry.field
    def tests(self, test_result: Optional[TestResult] = None, days_threshold: Optional[int] = None) -> List[UserTest]:
        return get_tests(test_result, days_threshold)

    @strawberry.field
    def locations(self) -> List[UserLocation]:
        return get_locations()

    @strawberry.field
    def trace_result(
        self,
        trace_input: TraceInput,
    ) -> TraceResult:

        radius = trace_input.radius or DAYS_THRESHOLD
        days = trace_input.days or RADIUS_THRESHOLD

        location = Location(trace_input.latitude, trace_input.longitude)
        sources = get_possible_exposure(location, radius, days)
        return TraceResult(
            is_exposed=len(sources) > 0,
            sources=sources,
        )


schema = strawberry.Schema(query=Query)
