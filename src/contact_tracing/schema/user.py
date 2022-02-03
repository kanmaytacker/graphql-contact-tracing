import strawberry


@strawberry.type
class User:
    id: int
    first_name: str
    last_name: str
    email: str
