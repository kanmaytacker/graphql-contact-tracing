from haversine import Unit, haversine

from contact_tracing.schema.user_location import Location


def haversine_distance(location1: Location, location2: Location) -> float:
    return haversine((location1.lat, location1.lng), (location2.lat, location2.lng), unit=Unit.METERS)
