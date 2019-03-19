# Standard library
import logging
from typing import Any, Dict, Optional

# 3rd party modules
import flask
from flask import jsonify, make_response, request

# Internal modules
from app.config import status
from app.error import BadRequestError
from app.instrumentation import trace
from app.models.dto import NewUserRequest
from app.service import user_service, health


_log = logging.getLogger(__name__)


@trace
def create_user() -> flask.Response:
    body = _get_request_body("username", "password", "repPassword")
    user_req = NewUserRequest.fromdict(body)
    login_res = user_service.create_user(user_req)
    return _create_response(login_res.todict())


@trace
def check_health() -> flask.Response:
    health_status = health.check()
    return _create_response(health_status)


### Private utility functions ###


def _get_request_body(*required_fields: str) -> Dict[str, Any]:
    """Gets flask request body as dict and optionally verifies that field names are present

    :param required_fields: Optional list of required field names.
    :return: Request body.
    """
    body = request.get_json(silent=True)
    for field in required_fields:
        if field not in body:
            raise BadRequestError(message=f"Missing required field: {field}")
    return body


def _get_param(name: str, default: Optional[str]) -> str:
    """Gets a request parameter with an optional default.
    If no parameter is found and the defualt is none a BadRequestError is thown.

    :param name: Name of the parameter to get.
    :param default: Optional default value.
    :return: Value.
    """
    value = request.args.get(name, default)
    if not value:
        raise BadRequestError(message=f"Missing {name} param")
    return value


def _create_response(
    result: Dict[str, Any], status: int = status.HTTP_200_OK
) -> flask.Response:
    """Returns a response indicating that an index update was triggered.

    :return: flask.Response.
    """
    return make_response(jsonify(result), status)


def _create_ok_response() -> flask.Response:
    """Creates a 200 OK response.

    :return: flask.Response.
    """
    ok_body: Dict[str, str] = {"status": "OK"}
    return make_response(jsonify(ok_body), status.HTTP_200_OK)
