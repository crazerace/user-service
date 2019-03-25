# Standard library
from datetime import datetime

# 3rd party modules
from crazerace.http import status

# Intenal modules
from app.models import User
from tests import TestEnvironment, JSON, new_id, headers


def test_search_user():
    user_1_id = new_id()
    user_2_id = new_id()
    user_3_id = new_id()
    user_4_id = new_id()
    users = [
        User(
            id=user_1_id,
            username="tobbe",
            password="h-p-1",
            salt="salt-1",
            created_at=datetime.utcnow(),
        ),
        User(
            id=user_2_id,
            username="tobias",
            password="h-p-1",
            salt="salt-1",
            created_at=datetime.utcnow(),
        ),
        User(
            id=user_3_id,
            username="toby",
            password="h-p-1",
            salt="salt-1",
            created_at=datetime.utcnow(),
        ),
        User(
            id=user_4_id,
            username="simon",
            password="h-p-1",
            salt="salt-1",
            created_at=datetime.utcnow(),
        ),
    ]

    with TestEnvironment(items=users) as client:
        unauth_res = client.get(f"/v1/users?query=tob", content_type=JSON)
        assert unauth_res.status_code == status.HTTP_401_UNAUTHORIZED

        res = client.get(
            f"/v1/users?query=tob", headers=headers(new_id()), content_type=JSON
        )
        assert res.status_code == status.HTTP_200_OK
        results = res.get_json()["results"]
        assert len(results) == 3
        assert results[0]["id"] == user_1_id
        assert results[0]["username"] == "tobbe"
        assert results[1]["id"] == user_2_id
        assert results[1]["username"] == "tobias"
        assert results[2]["id"] == user_3_id
        assert results[2]["username"] == "toby"

        res = client.get(
            f"/v1/users?query=tob;", headers=headers(new_id()), content_type=JSON
        )
        assert res.status_code == status.HTTP_200_OK
        assert len(res.get_json()["results"]) == 3

        invalid_res = client.get(
            f"/v1/users", headers=headers(new_id()), content_type=JSON
        )
        assert invalid_res.status_code == status.HTTP_400_BAD_REQUEST

