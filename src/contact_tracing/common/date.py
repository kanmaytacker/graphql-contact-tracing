"""Utility methods for working with dates."""
from datetime import datetime


def difference_in_days(date1: datetime, date2: datetime) -> int:
    """Calculates the difference in days between two dates.

    Args:
        date1 (datetime): The first date.
        date2 (datetime): The second date.

    Returns:
        int: The difference in days.
    """
    return (date2 - date1).days
