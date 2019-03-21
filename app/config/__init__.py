# Standard library
import os
from logging.config import dictConfig

# Internal modules
from .logging import LOGGING_CONIFG


dictConfig(LOGGING_CONIFG)


SERVICE_NAME: str = "user-service"
SERVICE_VERSION: str = "0.1"
SERVER_NAME: str = f"{SERVICE_NAME}/{SERVICE_VERSION}"
TEST_MODE: bool = os.getenv("TEST_MODE", "0") == "1"
DATETIME_FORMAT: str = "%Y-%m-%d %H:%M:%S.%f"
MIN_PASSWORD_LENGTH: int = 8
SALT_LENGTH: int = 24
PASSWORD_PEPPER: bytes = os.environ["PASSWORD_PEPPER"].encode()
JWT_SECRET: str = os.environ["JWT_SECRET"]


class AppConfig:
    SQLALCHEMY_DATABASE_URI: str = "sqlite:///:memory:"
    SQLALCHEMY_TRACK_MODIFICATIONS: bool = False

