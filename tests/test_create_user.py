# Standard library
import hashlib
import hmac
import json

# 3rd party modules
from crazerace import jwt
from crazerace.http import status

# Intenal modules
from app.repository import user_repo
from app.config import JWT_SECRET
from tests import TestEnvironment, JSON


def test_create_user():
    with TestEnvironment() as client:
        req_body = json.dumps(
            {"username": "user1", "password": "valid-pwd", "repPassword": "valid-pwd"}
        )
        res = client.post("/v1/users", data=req_body, content_type=JSON)
        assert res.status_code == status.HTTP_200_OK
        user = user_repo.find_by_username("user1")
        assert user is not None
        assert user.username == "user1"
        assert not user.archived
        assert user.archived_at is None
        assert user.role == "USER"
        assert isinstance(user.password, str) and len(user.password) > 0
        assert isinstance(user.salt, str) and len(user.salt) > 0
        assert len(user.renew_tokens) == 1
        renew_token = user.renew_tokens[0]
        assert not renew_token.used
        assert len(renew_token.token) == 64
        assert renew_token.user_id == user.id
        assert renew_token.created_at < renew_token.valid_to

        login_res = res.get_json()
        assert login_res["userId"] == user.id
        _assert_renew_token(login_res["renewToken"], renew_token.token)
        token_body = jwt.decode(login_res["token"], JWT_SECRET)
        assert token_body.subject == user.id
        assert token_body.role == "USER"

        duplicate = json.dumps(
            {
                "username": "user1",
                "password": "other-ok-pwd",
                "repPassword": "other-ok-pwd",
            }
        )
        res = client.post("/v1/users", data=duplicate, content_type=JSON)
        assert res.status_code == status.HTTP_409_CONFLICT
        assert len(user_repo.find_by_username("user1").renew_tokens) == 1


def test_new_user_not_enough_info():
    with TestEnvironment() as client:
        req_body = json.dumps({"username": "some-username"})
        res = client.post("/v1/users", data=req_body, content_type=JSON)
        assert res.status_code == status.HTTP_400_BAD_REQUEST

        req_body = json.dumps({"password": "some-password"})
        res = client.post("/v1/users", data=req_body, content_type=JSON)
        assert res.status_code == status.HTTP_400_BAD_REQUEST

        req_body = json.dumps({"username": 1, "password": "some-drowssap"})
        res = client.post("/v1/users", data=req_body, content_type=JSON)
        assert res.status_code == status.HTTP_400_BAD_REQUEST

        req_body = json.dumps({"username": "user", "password": "some-drowssap"})
        res = client.post("/v1/users", data=req_body, content_type=JSON)
        assert res.status_code == status.HTTP_400_BAD_REQUEST


def test_invalid_password():
    with TestEnvironment() as client:
        req_body = json.dumps(
            {"username": "user", "password": "short", "repPassword": "short"}
        )
        res = client.post("/v1/users", data=req_body, content_type=JSON)
        assert res.status_code == status.HTTP_400_BAD_REQUEST

        req_body = json.dumps(
            {"username": "user", "password": "shortest", "repPassword": "tsetrohs"}
        )
        res = client.post("/v1/users", data=req_body, content_type=JSON)
        assert res.status_code == status.HTTP_400_BAD_REQUEST


def _assert_renew_token(raw: str, stored: str) -> None:
    assert len(raw) == 100
    assert len(stored) == 64
    assert not stored in raw
    hashed = hmac.new(JWT_SECRET.encode(), raw.encode(), hashlib.sha256).hexdigest()
    assert hashed == stored
