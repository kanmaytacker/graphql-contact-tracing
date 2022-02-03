from pytest import fixture

from contact_tracing.mock.user_locations import locations as user_locations


@fixture
def location():
    return user_locations[0]

@fixture
def locations():
    return user_locations