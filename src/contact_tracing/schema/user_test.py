from datetime import datetime
from enum import Enum, auto

import strawberry


@strawberry.enum
class TestResult(Enum):
    POSITIVE = auto()
    NEGATIVE = auto()
    VOID = auto()


@strawberry.type
class UserTest:
    id: int
    test_id: str
    user_id: int
    test_result: TestResult
    timestamp: datetime
