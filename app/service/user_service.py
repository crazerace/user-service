# Standard library
import hashlib
import hmac
import secrets
from uuid import uuid4
from typing import Tuple

# 3rd party libraries
from argon2 import PasswordHasher
from crazerace import jwt
from crazerace.http.error import BadRequestError
from crazerace.http.instrumentation import trace

# Internal modules
from app.config import MIN_PASSWORD_LENGTH, SALT_LENGTH, PASSWORD_PEPPER, JWT_SECRET
from app.models import User
from app.models.dto import NewUserRequest, LoginResponse
from app.repository import user_repo


_password_hasher = PasswordHasher()


@trace("user_service")
def create_user(req: NewUserRequest) -> LoginResponse:
    validate_password(req)
    password_hash, salt = hash_password(req.password)
    user = User(id=_new_id(), username=req.username, password=password_hash, salt=salt)
    user_repo.save(user)
    jwt_token = jwt.create_token(user.id, "USER", JWT_SECRET)
    return LoginResponse(user_id=user.id, token=jwt_token)


@trace("user_service")
def archive_user(id: str) -> None:
    user = _must_get_user(id)
    archive_id = f"archived-{user.id}"
    user_repo.archive(user, archive_id)
    print(user)


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


def _must_get_user(id: str) -> User:
    user = user_repo.find(id)
    if not user or user.archived:
        raise BadRequestError("No such active user")
    return user


### Private utility functions ###


def _new_id() -> str:
    return str(uuid4()).lower()
