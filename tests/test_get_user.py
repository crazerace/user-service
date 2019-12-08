# Standard library
from datetime import datetime

# 3rd party modules
from crazerace.http import status

# Intenal modules
from app.models import User
from tests import TestEnvironment, JSON, new_id, headers


def test_get_user():
    user_1_id = new_id()
    user_2_id = new_id()
    archived_user_id = new_id()
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
            username="simon",
            password="h-p-1",
            salt="salt-1",
            created_at=datetime.utcnow(),
        ),
        User(
            id=archived_user_id,
            username=f"archived-{archived_user_id}",
            password="h-p-1",
            salt="salt-1",
            archived=True,
            created_at=datetime.utcnow(),
            archived_at=datetime.utcnow(),
        ),
    ]

    with TestEnvironment(items=users) as client:
        unauth_res = client.get(f"/v1/users/{new_id()}", content_type=JSON)
        assert unauth_res.status_code == status.HTTP_401_UNAUTHORIZED

        res_missing = client.get(
            f"/v1/users/{new_id()}", headers=headers(new_id()), content_type=JSON
        )
        assert res_missing.status_code == status.HTTP_404_NOT_FOUND

        res_1 = client.get(
            f"/v1/users/{user_1_id}", headers=headers(new_id()), content_type=JSON
        )
        assert res_1.status_code == status.HTTP_200_OK
        body_1 = res_1.get_json()
        assert body_1["id"] == user_1_id
        assert body_1["username"] == "tobbe"
        assert "createdAt" in body_1
        assert len(body_1) == 3

        res_2 = client.get(
            f"/v1/users/{user_2_id}", headers=headers(new_id()), content_type=JSON
        )
        assert res_2.status_code == status.HTTP_200_OK
        body_2 = res_2.get_json()
        assert body_2["id"] == user_2_id
        assert body_2["username"] == "simon"
        assert "createdAt" in body_2
        assert len(body_2) == 3

        res_archived = client.get(
            f"/v1/users/{archived_user_id}", headers=headers(new_id()), content_type=JSON
        )
        assert res_archived.status_code == status.HTTP_404_NOT_FOUND
