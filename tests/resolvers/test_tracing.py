from typing import Any, Dict, List

import pytest

from contact_tracing.common.config import DEFAULT_DAYS_THRESHOLD, DEFAULT_RADIUS
from contact_tracing.resolvers.tracing import get_possible_exposure
from contact_tracing.schema.user_location import Location


@pytest.mark.usefixtures("locations")
def test_possible_exposure(locations: List[Dict[str, Any]]) -> None:

    selected_user_id = 2
    selected_user_coordinates = next(filter(lambda location: location["user_id"] == selected_user_id, locations))

    selected_user_location = Location(**selected_user_coordinates["location"])

    sources = get_possible_exposure(selected_user_location, DEFAULT_RADIUS, DEFAULT_DAYS_THRESHOLD)

    expected_source_id = 1
    assert len(sources), "If the selected user was near to other positive users, there should be at least one source"
    assert (
        sources[0].id == expected_source_id
    ), "If the user was near to other positive users, the first source should be the user ID {expected_source_id}".format(
        expected_source_id=expected_source_id
    )


def test_no_exposure() -> None:

    selected_user_location = Location(lat=0, lng=0)

    sources = get_possible_exposure(selected_user_location, DEFAULT_RADIUS, DEFAULT_DAYS_THRESHOLD)
    assert not len(sources), "If the selected location was not near to other positive users, there should be no sources"
