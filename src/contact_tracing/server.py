"""Entry point for the application."""
import uvicorn
from fastapi import FastAPI
from starlette.responses import RedirectResponse
from strawberry.asgi import GraphQL

from contact_tracing.common.config import DEBUG, HOST, PORT, PROJECT_NAME, RELOAD, VERSION
from contact_tracing.schema.schema import schema


def get_application() -> FastAPI:
    """Creates an instance of the Fast API application.

    Returns:
        FastAPI: A configured FastAPI instance
    """
    return FastAPI(title=PROJECT_NAME, debug=DEBUG, version=VERSION)


app = get_application()
graphql_app = GraphQL(schema)
app.add_route("/graphql", graphql_app)


@app.get("/")
async def redirect() -> RedirectResponse:
    """Redirects to the GraphQL endpoint.

    Returns:
        RedirectResponse: A redirect response to the GraphQL endpoint.
    """
    return RedirectResponse(url="/graphql")


def main() -> int:
    """The main entry point for the application.

    Returns:
        int: The exit code for the application.
    """
    uvicorn.run(app, host=HOST, port=PORT, reload=RELOAD, debug=DEBUG)
    return 0
