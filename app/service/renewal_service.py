# Standard library
import secrets
from datetime import datetime, timedelta

# 3rd party libraries
from crazerace.http.error import BadRequestError, UnauthorizedError
from crazerace.http.instrumentation import trace

# Internal modules
from app.config import RENEWAL_TOKEN_LENGTH
from app.models import RenewToken
from app.service import auth_log
from app.repository import renew_token_repo


@trace("renewal_service")
def create_token(user_id: str) -> RenewToken:
    token = RenewToken(
        token=_generate_token(),
        user_id=user_id,
        valid_to=datetime.utcnow() + timedelta(days=365),
    )
    renew_token_repo.save(token)
    return token


def _generate_token() -> str:
    return secrets.token_hex(RENEWAL_TOKEN_LENGTH)
