"""Utility methods for working with geographical distances."""
from haversine import Unit, haversine

from contact_tracing.schema.user_location import Location


def haversine_distance(location1: Location, location2: Location) -> float:
    """Calculates the distance between two locations using the haversine formula.

    Args:
        location1 (Location): The first location.
        location2 (Location): The second location.

    Returns:
        float: The distance in meters.
    """
    return haversine((location1.lat, location1.lng), (location2.lat, location2.lng), unit=Unit.METERS)
