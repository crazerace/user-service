# Standard library
import json
import logging
from typing import Dict, Tuple

# 3rd party modules
import flask

# Internal modules
from app import db
from app.error import ServiceUnavilableError


_log = logging.getLogger(__name__)


def check() -> Dict[str, str]:
    db_msg, db_ok = _db_connected()
    if not db_ok:
        message = f"Health check failed. db={db_msg}"
        _log.error(message)
        raise ServiceUnavilableError(message)
    return {"db": db_msg, "status": "UP"}


def _db_connected() -> Tuple[str, bool]:
    try:
        db.engine.execute("SELECT 1")
        return "UP", True
    except Exception as e:
        _log.error(str(e))
        return "DOWN", True
