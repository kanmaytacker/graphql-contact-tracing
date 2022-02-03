from pytest import fixture

from contact_tracing.mock.users import users


@fixture
def user():
    return users[0]

@fixture
def users():
    return users