# Standard library
import json

# 3rd party modules
from crazerace.http import status

# Intenal modules
from app.repository import user_repo
from app.config import JWT_SECRET
from tests import TestEnvironment, JSON


def test_renew_token():
    with TestEnvironment() as client:
        req_body = json.dumps(
            {"username": "renewUser", "password": "valid-pwd", "repPassword": "valid-pwd"}
        )
        res_1 = client.post("/v1/users", data=req_body, content_type=JSON)
        assert res_1.status_code == status.HTTP_200_OK
        login_res = res_1.get_json()
        user_id = login_res["userId"]
        first_renew_token = login_res["renewToken"]
        user = user_repo.find_by_username("renewUser")
        assert user.id == user_id
        assert len(user.renew_tokens) == 1
        assert not user.renew_tokens[0].used
        assert user.renew_tokens[0].token == first_renew_token
        assert len(user.auth_events) == 1
        assert user.auth_events[0].event_type == "SIGN_UP"

        renew_body = json.dumps({"userId": user_id, "token": first_renew_token})
        res_2 = client.post("/v1/renew", data=renew_body, content_type=JSON)
        assert res_2.status_code == status.HTTP_200_OK
        renew_res = res_2.get_json()
        second_renew_token = renew_res["renewToken"]
        user = user_repo.find_by_username("renewUser")
        assert user.id == user_id
        assert len(user.renew_tokens) == 2
        assert user.renew_tokens[0].used
        assert not user.renew_tokens[1].used
        assert user.renew_tokens[1].token == second_renew_token
        assert len(user.auth_events) == 2
        assert user.auth_events[1].succeeded
        assert user.auth_events[1].event_type == "RENEW"

        res_3 = client.post("/v1/renew", data=renew_body, content_type=JSON)
        assert res_3.status_code == status.HTTP_401_UNAUTHORIZED
        user = user_repo.find_by_username("renewUser")
        assert len(user.auth_events) == 3
        assert not user.auth_events[2].succeeded
        assert user.auth_events[2].event_type == "RENEW"
