# Standard library
import hashlib
import hmac
import secrets
import logging
from uuid import uuid4
from typing import Tuple

# 3rd party libraries
from argon2 import PasswordHasher
from crazerace import jwt
from crazerace.http.error import BadRequestError, UnauthorizedError
from crazerace.http.instrumentation import trace

# Internal modules
from app.config import MIN_PASSWORD_LENGTH, SALT_LENGTH, PASSWORD_PEPPER, JWT_SECRET
from app.models import User
from app.models.dto import NewUserRequest, LoginResponse, LoginRequest
from app.repository import user_repo


_password_hasher = PasswordHasher()
_log = logging.getLogger(__name__)

@trace("user_service")
def create_user(req: NewUserRequest) -> LoginResponse:
    validate_password(req)
    password_hash, salt = hash_password(req.password)
    user = User(id=_new_id(), username=req.username, password=password_hash, salt=salt)
    user_repo.save(user)
    jwt_token = jwt.create_token(user.id, "USER", JWT_SECRET)
    return LoginResponse(user_id=user.id, token=jwt_token)


@trace("user_service")
def login_user(req: LoginRequest) -> LoginResponse:
    user = user_repo.find_by_username(req.username)
    if not user:
        raise UnauthorizedError("Username and password doesn't match.")
    verify_password(req.password, user)
    jwt_token = jwt.create_token(user.id, "USER", JWT_SECRET)
    return LoginResponse(user_id=user.id, token=jwt_token)


def validate_password(user: NewUserRequest) -> None:
    if len(user.password) < MIN_PASSWORD_LENGTH:
        raise BadRequestError("Password too short")
    elif user.password != user.rep_password:
        raise BadRequestError("Passwords don't match")


def verify_password(password: str, user: User) -> None:
    password_mac = _salt_password(password, user.salt)
    try:
        _password_hasher.verify(user.password, password_mac)
    except Exception as e:
        _log.info(f"password could not be verified. Error: {str(e)}")
        raise UnauthorizedError("Username and password doesn't match.")


def hash_password(password: str) -> Tuple[str, str]:
    salt = secrets.token_hex(SALT_LENGTH)
    password_mac = _salt_password(password, salt)
    password_hash = _password_hasher.hash(password_mac)
    return password_hash, salt


def _salt_password(password: str, salt: str) -> str:
    content = f"{salt}-{password}".encode()
    return hmac.new(PASSWORD_PEPPER, content, hashlib.sha256).hexdigest()


### Private utility functions ###


def _new_id() -> str:
    return str(uuid4()).lower()
