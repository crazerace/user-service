# Standard libraries
import json

# 3rd party modules
from crazerace import jwt
from crazerace.http import status

# Intenal modules
from app.repository import user_repo
from app.config import JWT_SECRET
from tests import TestEnvironment, JSON


def test_login_user():
    with TestEnvironment() as client:
        req_body = json.dumps(
            {"username": "user1", "password": "valid-pwd", "repPassword": "valid-pwd"}
        )
        res = client.post("/v1/users", data=req_body, content_type=JSON)
        assert res.status_code == status.HTTP_200_OK
        auth_events = user_repo.find_by_username("user1").auth_events
        assert len(auth_events) == 1
        assert auth_events[0].event_type == "SIGN_UP"
        assert auth_events[0].succeeded
        assert _is_ipv4(auth_events[0].ip_address)

        req_body = json.dumps({"username": "user1", "password": "valid-pwd"})
        res = client.post("/v1/login", data=req_body, content_type=JSON)
        assert res.status_code == status.HTTP_200_OK
        user = user_repo.find_by_username("user1")
        login_res = res.get_json()
        assert login_res["userId"] == user.id
        token_body = jwt.decode(login_res["token"], JWT_SECRET)
        assert token_body.subject == user.id
        assert token_body.role == "USER"
        auth_events = user.auth_events
        assert len(auth_events) == 2
        assert auth_events[1].user_id == user.id
        assert auth_events[1].event_type == "LOGIN"
        assert auth_events[1].succeeded
        assert _is_ipv4(auth_events[1].ip_address)

        assert len(user.renew_tokens) == 2
        renew_token = user.renew_tokens[1]
        assert not renew_token.used
        assert len(renew_token.token) == 100
        assert renew_token.user_id == user.id
        assert renew_token.created_at < renew_token.valid_to


def test_login_user_incorrect_values():
    with TestEnvironment() as client:
        req_body = json.dumps(
            {"username": "user1", "password": "valid-pwd", "repPassword": "valid-pwd"}
        )
        res = client.post("/v1/users", data=req_body, content_type=JSON)
        assert res.status_code == status.HTTP_200_OK
        user_id = res.get_json()["userId"]
        user = user_repo.find(user_id)
        auth_events = user.auth_events
        assert len(auth_events) == 1
        assert auth_events[0].event_type == "SIGN_UP"
        assert auth_events[0].succeeded
        assert _is_ipv4(auth_events[0].ip_address)
        assert len(user.renew_tokens) == 1

        # Existing username incorrect pw
        req_body = json.dumps({"username": "user1", "password": "invalid-pwd"})
        res = client.post("/v1/login", data=req_body, content_type=JSON)
        assert res.status_code == status.HTTP_401_UNAUTHORIZED
        user = user_repo.find_by_username("user1")
        auth_events = user.auth_events
        assert len(auth_events) == 2
        assert auth_events[1].user_id == user_id
        assert auth_events[1].event_type == "LOGIN"
        assert not auth_events[1].succeeded
        assert _is_ipv4(auth_events[1].ip_address)

        # correct username incorrect pw type
        req_body = json.dumps({"username": "user1", "password": 12323445})
        res = client.post("/v1/login", data=req_body, content_type=JSON)
        assert res.status_code == status.HTTP_400_BAD_REQUEST

        # incorrect username
        req_body = json.dumps({"username": "userDoesntExist", "password": "valid-pwd"})
        res = client.post("/v1/login", data=req_body, content_type=JSON)
        assert res.status_code == status.HTTP_401_UNAUTHORIZED
        user = user_repo.find(user_id)
        assert len(user.auth_events) == 2
        assert len(user.renew_tokens) == 1
        renew_token = user.renew_tokens[0]
        assert not renew_token.used


def _is_ipv4(ip_address: str) -> bool:
    octets = ip_address.split(".")
    if len(octets) != 4:
        return False
    for octet in [int(o) for o in octets]:
        if octet < 0 or octet > 255:
            return False
    return True
