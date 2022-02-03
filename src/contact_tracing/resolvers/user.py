"""Resolver functions for the User type."""
from typing import List, Optional

from contact_tracing.mock.users import users
from contact_tracing.schema.user import User


def get_users(include: List[int] = None) -> List[User]:
    """Resolver function to fetch all users from the database.

    TODO:
         - Currently fetches from mock data. Move to database.
         - Add pagination and offset
         - Add more filters

     Args:
         include (List[int]): A list of user ids to filter the results on.

     Returns:
         List[User]: A list of users.
    """
    parsed_users = map(lambda user: User(**user), users)
    if not include:
        return list(parsed_users)

    return list(filter(lambda user: user.id in include, parsed_users))


def get_user(id: int) -> Optional[User]:
    """Resolver function to fetch a user from the database.

    Args:
        id (int): The id of the user to fetch.

    Returns:
        Optional[User]: The user with the given id.
    """
    return next((user for user in get_users() if user.id == id), None)
