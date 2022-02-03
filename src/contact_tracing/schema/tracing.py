from typing import List, Optional

import strawberry

from .user import User
from contact_tracing.common.config import DEFAULT_RADIUS, DEFAULT_DAYS_THRESHOLD

@strawberry.type
class TraceResult:
    is_exposed: bool
    sources: List[User]


@strawberry.input
class TraceInput:
    latitude: float
    longitude: float
    radius: Optional[float] = DEFAULT_RADIUS
    days: Optional[int] = DEFAULT_DAYS_THRESHOLD
