# Standard library
import json

# Intenal modules
from app.config import status
from app.repository import user_repo
from tests import TestEnvironment, JSON


def test_creaate_user():
    with TestEnvironment() as client:
        req_body = json.dumps(
            {"username": "user1", "password": "valid-pwd", "repPassword": "valid-pwd"}
        )
        res = client.post("/v1/users", data=req_body, content_type=JSON)
        assert res.status_code == status.HTTP_200_OK
        user = user_repo.find_by_username("user1")
        assert user is not None
        assert user.username == "user1"

        req_body = json.dumps(
            {
                "username": "user1",
                "password": "other-ok-pwd",
                "repPassword": "other-ok-pwd",
            }
        )
        res = client.post("/v1/users", data=req_body, content_type=JSON)
        assert res.status_code == status.HTTP_409_CONFLICT


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
