# Standard libraries
import logging

# Internal modules
from app import db
from app.models import User
from .util import handle_error

_log = logging.getLogger(__name__)

@handle_error(logger=_log)
def save(user: User) -> None:
	db.session.add(user)
	db.session.commit()