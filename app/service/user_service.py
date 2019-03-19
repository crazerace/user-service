# Standard library
from uuid import uuid4
from typing import Tuple

# Internal modules
from app.config import MIN_PASSWORD_LENGTH
from app.error import BadRequestError
from app.instrumentation import trace
from app.models import User
from app.models.dto import NewUserRequest
from app.repository import user_repo


@trace
def create_user(req: NewUserRequest) -> None:
    validate_password(req)
    password_hash, salt = hash_password(req.password)
    user = User(id=_new_id(), username=req.username, password=password_hash, salt=salt)
    user_repo.save(user)


def validate_password(user: NewUserRequest) -> None:
    if len(user.password) < MIN_PASSWORD_LENGTH:
        raise BadRequestError("Password too short")
    elif user.password != user.rep_password:
        raise BadRequestError("Passwords don't match")


def hash_password(password: str) -> Tuple[str, str]:
    return "", ""


### Private utility functions ###


def _new_id() -> str:
    return str(uuid4()).lower()
