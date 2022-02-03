"""Entry point for the application."""
import uvicorn
from fastapi import FastAPI
from strawberry.asgi import GraphQL

from .common.config import DEBUG, HOST, PORT, PROJECT_NAME, RELOAD, VERSION
from .schema.schema import schema


def get_application() -> FastAPI:
    """Creates an instance of the Fast API application.

    Returns:
        FastAPI: A configured FastAPI instance
    """
    return FastAPI(title=PROJECT_NAME, debug=DEBUG, version=VERSION)


app = get_application()
graphql_app = GraphQL(schema)
app.add_route("/graphql", graphql_app)


def main() -> int:
    """The main entry point for the application.

    Returns:
        int: The exit code for the application.
    """
    uvicorn.run(app, host=HOST, port=PORT, reload=RELOAD, debug=DEBUG)
    return 0
