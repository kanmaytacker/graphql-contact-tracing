"""GraphQL schema for the location object."""
from datetime import datetime

import strawberry


@strawberry.type
class Location:
    """GraphQL type for location coordinates."""

    lat: float
    lng: float


@strawberry.type
class UserLocation:
    """GraphQL type for user locations."""

    id: int  # noqa: A003, VNE003
    user_id: int
    timestamp: datetime
    location: Location
