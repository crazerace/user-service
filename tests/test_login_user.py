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


        req_body = json.dumps(
            {"username": "user1", "password": "valid-pwd"}
        )
        res = client.post("/v1/login", data=req_body, content_type=JSON)
        assert res.status_code == status.HTTP_200_OK
        user = user_repo.find_by_username("user1")
        login_res = res.get_json()
        assert login_res["userId"] == user.id
        token_body = jwt.decode(login_res["token"], JWT_SECRET)
        assert token_body.subject == user.id
        assert token_body.role == "USER"


def test_login_user_incorrect_values():
	with TestEnvironment() as client:
		req_body = json.dumps(
            {"username": "user1", "password": "valid-pwd", "repPassword": "valid-pwd"}
        )
        res = client.post("/v1/users", data=req_body, content_type=JSON)
        assert res.status_code == status.HTTP_200_OK


        # Existing username incorrect pw
        req_body = json.dumps(
            {"username": "user1", "password": "invalid-pwd"}
        )
        res = client.post("/v1/login", data=req_body, content_type=JSON)
        assert res.status_code == status.HTTP_401_UNAUTHORIZED


        #correct username incorrect pw type
        req_body = json.dumps(
            {"username": "user1", "password": 12323445}
        )
        res = client.post("/v1/login", data=req_body, content_type=JSON)
        assert res.status_code == status.HTTP_400_BADREQUEST


        #incorrect username
        req_body = json.dumps(
            {"username": "userDoesntExist", "password": "valid-pwd"}
        )
        res = client.post("/v1/login", data=req_body, content_type=JSON)
        assert res.status_code == status.HTTP_401_UNAUTHORIZED