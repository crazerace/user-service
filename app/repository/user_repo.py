# Standard libraries
import logging
from datetime import datetime
from typing import Optional

# 3rd party libraries
from crazerace.http.error import ConflictError
from crazerace.http.instrumentation import trace

# Internal modules
from app import db
from app.models import User
from .util import handle_error


_log = logging.getLogger(__name__)


@trace("user_repo")
@handle_error(logger=_log, integrity_error_class=ConflictError)
def save(user: User) -> None:
    db.session.add(user)
    db.session.commit()


@trace("user_repo")
def find_by_username(username: str) -> Optional[User]:
    return User.query.filter(User.username == username).first()


@trace("user_repo")
def find(id: str) -> Optional[User]:
    return User.query.filter(User.id == id).first()


@trace("user_repo")
def archive(user: User, archive_id: str) -> None:
    user.username = archive_id
    user.password = ""
    user.salt = ""
    user.archived = True
    user.archived_at = datetime.utcnow()
    db.session.flush()
    db.session.commit()
