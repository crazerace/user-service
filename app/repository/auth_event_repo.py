# Standard libraries
import logging
from datetime import datetime
from typing import List, Optional

# 3rd party libraries
from crazerace.http.error import ConflictError
from crazerace.http.instrumentation import trace

# Internal modules
from app import db
from app.models import AuthEvent
from .util import handle_error, sanitize_string


_log = logging.getLogger(__name__)


@trace("auth_event_repo")
@handle_error(logger=_log, integrity_error_class=ConflictError)
def save(event: AuthEvent) -> None:
    db.session.add(event)
    db.session.commit()