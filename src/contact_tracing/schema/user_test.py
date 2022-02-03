"""GraphQL schema for the test object."""
from datetime import datetime
from enum import Enum, auto

import strawberry


@strawberry.enum
class TestResult(Enum):
    """GraphQL enum for test results."""

    POSITIVE = auto()  # noqa: WPS115
    NEGATIVE = auto()  # noqa: WPS115
    VOID = auto()  # noqa: WPS115


@strawberry.type
class UserTest:
    """GraphQL type for user tests."""

    id: int  # noqa: A003, VNE003
    test_id: str
    user_id: int
    test_result: TestResult
    timestamp: datetime
