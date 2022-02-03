from pytest import fixture

from contact_tracing.mock.user_tests import tests as user_tests


@fixture
def test():
    return user_tests[0]

@fixture
def tests():
    return user_tests