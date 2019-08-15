# Standard library
import hashlib
import hmac
import secrets
from datetime import datetime, timedelta
from typing import Tuple

# 3rd party libraries
from crazerace import jwt
from crazerace.http.error import BadRequestError, UnauthorizedError
from crazerace.http.instrumentation import trace

# Internal modules
from app.config import RENEWAL_TOKEN_LENGTH, JWT_SECRET
from app.models import User, RenewToken
from app.models.dto import RenewRequest, LoginResponse, ClientInfo
from app.service import auth_log
from app.repository import renew_token_repo, user_repo


@trace("renewal_service")
def create_token(user_id: str) -> str:
    raw_token = _generate_token()
    token = RenewToken(
        token=_hash(raw_token),
        user_id=user_id,
        valid_to=datetime.utcnow() + timedelta(days=365),
    )
    renew_token_repo.save(token)
    return raw_token


@trace("renewal_service")
def renew_token(request: RenewRequest, client: ClientInfo) -> LoginResponse:
    try:
        user, token = _find_user_and_token(request)
        _set_token_as_used(token)
        renew_token = create_token(user.id)
        jwt_token = jwt.create_token(user.id, user.role, JWT_SECRET)
        auth_log.record_renewal(user.id, client)
        return LoginResponse(user_id=user.id, token=jwt_token, renew_token=renew_token)
    except Exception as e:
        auth_log.record_renewal(request.user_id, client, success=False)
        raise e


def _find_user_and_token(request: RenewRequest) -> Tuple[User, RenewToken]:
    user = user_repo.find(request.user_id)
    if not user:
        raise UnauthorizedError()
    token = renew_token_repo.find_active(request.user_id, _hash(request.token))
    if not token:
        raise UnauthorizedError()
    return user, token


def _set_token_as_used(token: RenewToken) -> None:
    token.used = True
    token.valid_to = valid_to = datetime.utcnow() - timedelta(seconds=1)
    renew_token_repo.save(token)


def _generate_token() -> str:
    return secrets.token_hex(RENEWAL_TOKEN_LENGTH)


def _hash(token: str) -> str:
    return hmac.new(JWT_SECRET.encode(), token.encode(), hashlib.sha256).hexdigest()
