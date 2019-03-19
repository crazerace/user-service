# Standard libraries
import logging
from typing import Optional

# Internal modules
from app import db
from app.instrumentation import trace
from app.error import ConflictError
from app.models import User
from .util import handle_error

_log = logging.getLogger(__name__)


@handle_error(logger=_log, integrity_error_class=ConflictError)
def save(user: User) -> None:
    db.session.add(user)
    db.session.commit()


def find_by_username(username: str) -> Optional[User]:
    return User.query.filter(User.username == username).first()

