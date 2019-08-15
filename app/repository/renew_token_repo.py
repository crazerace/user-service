# Standard libraries
import logging
from datetime import datetime
from typing import Optional

# 3rd party libraries
from crazerace.http.error import ConflictError
from crazerace.http.instrumentation import trace

# Internal modules
from app import db
from app.models import RenewToken
from .util import handle_error


_log = logging.getLogger(__name__)


@trace("renew_token_repo")
@handle_error(logger=_log, integrity_error_class=ConflictError)
def save(token: RenewToken) -> None:
    db.session.add(token)
    db.session.commit()


@trace("renew_token_repo")
def find_active(user_id: str, token: str) -> Optional[RenewToken]:
    now = datetime.utcnow()
    return RenewToken.query.filter(
        RenewToken.user_id == user_id,
        RenewToken.token == token,
        RenewToken.valid_to > now,
        RenewToken.used == False,
    ).first()
