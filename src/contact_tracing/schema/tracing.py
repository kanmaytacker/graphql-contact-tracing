"""GraphQL schema for the tracing object."""
from typing import List, Optional

import strawberry

from contact_tracing.common.config import DEFAULT_DAYS_THRESHOLD, DEFAULT_RADIUS
from contact_tracing.schema.user import User


@strawberry.type
class TraceResult:
    """GraphQL type for tracing results."""

    is_exposed: bool
    sources: List[User]


@strawberry.input
class TraceInput:
    """GraphQL input type for tracing."""

    latitude: float
    longitude: float
    radius: Optional[float] = DEFAULT_RADIUS
    days: Optional[int] = DEFAULT_DAYS_THRESHOLD
