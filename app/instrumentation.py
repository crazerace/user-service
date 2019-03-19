# Standard library
import logging
from functools import wraps
from typing import Any, Callable

# 3rd party modules.
from flask import request

# Internal modules
from app.error import InternalServerError


_log = logging.getLogger("TraceLogger")


def get_request_id() -> str:
    try:
        return request.id
    except Exception as e:
        raise InternalServerError(f"Getting request id failed. Exception=[{e}]")


def trace(f: Callable) -> Callable:
    @wraps(f)
    def decorated(*args, **kwargs) -> Any:
        req_id = get_request_id()
        _log.info(f"function=[{f.__qualname__}] requestId=[{req_id}]")
        return f(*args, **kwargs)

    return decorated
