# Standard library
import json

# Intenal modules
from app.config import status
from tests import TestEnvironment, JSON


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
