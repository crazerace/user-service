# Standard library
import logging
from typing import Any, Dict, Optional

# 3rd party modules
import flask
from flask import jsonify, make_response, request
from crazerace import http
from crazerace.http import status
from crazerace.http.error import BadRequestError, ForbiddenError
from crazerace.http.instrumentation import trace

# Internal modules
from app.config import CLIENT_ID_HEADER, CLIENT_IP_HEADER
from app.models.dto import NewUserRequest, LoginRequest, ClientInfo, RenewRequest
from app.service import user_service, renewal_service, health


_log = logging.getLogger(__name__)


@trace("controller")
def create_user() -> flask.Response:
    body = http.get_request_body("username", "password", "repPassword")
    user_req = NewUserRequest.fromdict(body)
    login_res = user_service.create_user(user_req, _get_client_info())
    return http.create_response(login_res.todict())


@trace("controller")
def get_user(user_id: str) -> flask.Response:
    user = user_service.get_user(user_id)
    return http.create_response(user.todict())


@trace("controller")
def delete_user(user_id: str) -> flask.Response:
    _assert_can_modify_user(user_id)
    user_service.archive_user(user_id)
    return http.create_ok_response()


@trace("controller")
def login_user() -> flask.Response:
    body = http.get_request_body("username", "password")
    log_req = LoginRequest.fromdict(body)
    login_res = user_service.login_user(log_req, _get_client_info())
    return http.create_response(login_res.todict())


@trace("controller")
def renew_token() -> flask.Response:
    body = http.get_request_body("userId", "token")
    renew_request = RenewRequest.fromdict(body)
    res = renewal_service.renew_token(renew_request, _get_client_info())
    return http.create_response(res.todict())


@trace("controller")
def search_for_users() -> flask.Response:
    query: str = http.get_param("query")
    search_results = user_service.search_for_users(query)
    return http.create_response(search_results.todict())


def check_health() -> flask.Response:
    health_status = health.check()
    return http.create_response(health_status)


### Private functions ###


def _assert_can_modify_user(user_id: str) -> None:
    if request.user_id != user_id and request.role != "ADMIN":
        raise ForbiddenError()


def _get_client_info() -> ClientInfo:
    return ClientInfo(
        id=request.headers.get(CLIENT_ID_HEADER, "NOT_FOUND"),
        ip_address=request.headers.get(CLIENT_IP_HEADER, request.remote_addr),
    )
