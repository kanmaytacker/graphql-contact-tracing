"""GraphQL schema for the user object."""
import strawberry


@strawberry.type
class User:
    """GraphQL type for users."""

    id: int  # noqa: A003, VNE003
    first_name: str
    last_name: str
    email: str
