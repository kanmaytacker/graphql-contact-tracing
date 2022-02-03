"""Configuration for the pytest test suite."""
from glob import glob


def refactor(string: str) -> str:
    """Refactor a string to be used as a test name.

    Args:
        string (str): The string to refactor.

    Returns:
        str: The refactored string.
    """
    return string.replace("/", ".").replace("\\", ".").replace(".py", "")


pytest_plugins = [refactor(fixture) for fixture in glob("tests/fixtures/*.py") if "__" not in fixture]
