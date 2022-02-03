"""Configuration file for the application contact-tracing."""
from starlette.config import Config

DEFAULT_NAME = "contact-tracing"
DEFAULT_PORT = 8080
DEFAULT_HOST = "0.0.0.0"  # noqa: S104
DEFAULT_DAYS_THRESHOLD = 14
DEFAULT_RADIUS = 100

config = Config(".env")

VERSION = "0.1.0"
DEBUG: bool = config("DEBUG", cast=bool, default=False)
RELOAD: bool = config("RELOAD", cast=bool, default=False)

PROJECT_NAME: str = config("PROJECT_NAME", default=DEFAULT_NAME)

HOST: str = config("HOST", default=DEFAULT_HOST)
PORT: int = config("PORT", default=DEFAULT_PORT, cast=int)

DAYS_THRESHOLD: int = config("DAYS_THRESHOLD", default=DEFAULT_DAYS_THRESHOLD, cast=int)
RADIUS_THRESHOLD: int = config("RADIUS_THRESHOLD", default=DEFAULT_RADIUS, cast=float)
