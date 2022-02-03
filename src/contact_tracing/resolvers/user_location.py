"""Resolver functions for the UserLocation type."""
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional

from dateutil import parser

from contact_tracing.common.date import difference_in_days
from contact_tracing.common.distance import haversine_distance
from contact_tracing.mock.user_locations import locations
from contact_tracing.schema.user_location import Location, UserLocation


def get_locations() -> List[UserLocation]:
    """Resolver function to fetch all user locations from the database.

    TODO:
        - Currently fetches from mock data. Move to database.
        - Add pagination and offset

    Returns:
        List[UserLocation]: A list of user locations.
    """
    return list(map(to_location, locations))


def to_location(location: Dict[str, Any]) -> UserLocation:
    """Converts a dictionary to a UserLocation object.

    Args:
        location (Dict[str, Union[str, int, Dict]]): The dictionary to be converted.

    Returns:
        UserLocation: The converted UserLocation object.
    """
    user_location = location["location"]
    parsed_location = Location(lat=user_location["lat"], lng=user_location["lng"])

    timestamp = parser.parse(location["timestamp"])

    return UserLocation(id=location["id"], user_id=location["user_id"], location=parsed_location, timestamp=timestamp)


def get_location(location_id: int) -> Optional[UserLocation]:
    """Resolver function to fetch a user location from the database.

    Args:
        location_id (int): The id of the user location to be fetched.

    Returns:
        Optional[UserLocation]: The user location with the given id.
    """
    return next((location for location in get_locations() if location.id == location_id), None)


def get_nearby_locations(
    user_location: Location, radius: float, days_threshold: int, include: List[int]
) -> List[UserLocation]:
    """Methode to fetch nearby locations from the database.

    Args:
        user_location (Location): The input location.
        radius (float): The radius of the search.
        days_threshold (int): The time horizon.
        include (List[int]): The list of user ids to be included in the search.

    Returns:
        List[UserLocation]: A list of nearby locations.
    """
    candidates = filter(
        lambda location: is_user_valid(location.user_id, include)
        and is_time_valid(datetime.now(timezone.utc), location.timestamp, days_threshold)
        and is_distance_valid(user_location, location.location, radius),
        get_locations(),
    )
    return list(candidates)


def is_user_valid(user_id: int, include: List[int]) -> bool:
    """Filter function to check if a user is to be included in the search.

    Args:
        user_id (int): The id of the user to be checked.
        include (List[int]): The list of user ids to be included in the search.

    Returns:
        bool: True if the user is to be included in the search, else False.
    """
    return user_id in include


def is_time_valid(timestamp_one: datetime, timestamp_two: datetime, days_threshold: int) -> bool:
    """Filter function to check if a location update is lesser than the time horizon.

    Args:
        timestamp_one (datetime): The current timestamp.
        timestamp_two (datetime): The timestamp of the location update.
        days_threshold (int): The time horizon.

    Returns:
        bool: True if the location update is lesser than the time horizon, else False.
    """
    return abs(difference_in_days(timestamp_one, timestamp_two)) <= days_threshold


def is_distance_valid(location_one: Location, location_two: Location, radius: float) -> bool:
    """Filter function to check if a location is within the radius of the input location.

    Args:
        location_one (Location): The input location.
        location_two (Location): The location to be checked.
        radius (float): The radius of the search.

    Returns:
        bool: True if the location is within the radius of the input location, else False.
    """
    return haversine_distance(location_one, location_two) <= radius
