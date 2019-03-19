# Standard library
import hashlib
import hmac
import secrets
from uuid import uuid4
from typing import Tuple

# 3rd party libraries
from argon2 import PasswordHasher

# Internal modules
from app.config import MIN_PASSWORD_LENGTH, SALT_LENGTH, PASSWORD_PEPPER
from app.error import BadRequestError
from app.instrumentation import trace
from app.models import User
from app.models.dto import NewUserRequest, LoginResponse
from app.repository import user_repo


_password_hasher = PasswordHasher()


@trace
def create_user(req: NewUserRequest) -> LoginResponse:
    validate_password(req)
    password_hash, salt = hash_password(req.password)
    user = User(id=_new_id(), username=req.username, password=password_hash, salt=salt)
    user_repo.save(user)
    return LoginResponse(user_id=user.id, token="")


def validate_password(user: NewUserRequest) -> None:
    if len(user.password) < MIN_PASSWORD_LENGTH:
        raise BadRequestError("Password too short")
    elif user.password != user.rep_password:
        raise BadRequestError("Passwords don't match")


def hash_password(password: str) -> Tuple[str, str]:
    password_mac, salt = _salt_password(password)
    password_hash = _password_hasher.hash(password_mac)
    return password_hash, salt


def _salt_password(password: str) -> Tuple[str, str]:
    salt = secrets.token_hex(SALT_LENGTH)
    content = f"{salt}-{password}".encode()
    password_mac = hmac.new(PASSWORD_PEPPER, content, hashlib.sha256).hexdigest()
    return password_mac, salt


### Private utility functions ###


def _new_id() -> str:
    return str(uuid4()).lower()
