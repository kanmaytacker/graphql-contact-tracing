from datetime import datetime

import strawberry


@strawberry.type
class Location:
    lat: float
    lng: float


@strawberry.type
class UserLocation:
    id: int
    user_id: int
    timestamp: datetime
    location: Location
