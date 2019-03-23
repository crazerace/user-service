# Standard library
from datetime import datetime

# 3rd party modules
from crazerace import jwt
from crazerace.http import status

# Intenal modules
from app.models import User
from app.repository import user_repo
from app.config import JWT_SECRET
from tests import TestEnvironment, JSON, new_id, headers


def test_creaate_user():
    user_id = new_id()
    existing_user = User(
        id=user_id,
        username="user1",
        password="hashed_password",
        salt="random-salt",
        created_at=datetime.utcnow(),
    )
    with TestEnvironment(items=[existing_user]) as client:
        wrong_id = new_id()
        fail_res = client.delete(
            f"/v1/users/{wrong_id}", headers=headers(wrong_id), content_type=JSON
        )
        assert fail_res.status_code == status.HTTP_400_BAD_REQUEST

        res = client.delete(
            f"/v1/users/{user_id}", headers=headers(user_id), content_type=JSON
        )
        assert res.status_code == status.HTTP_200_OK
        deleted_user = user_repo.find(user_id)
        assert deleted_user is not None
        assert deleted_user.username == f"archived-{user_id}"
        assert deleted_user.archived
        assert deleted_user.password == ""
        assert deleted_user.salt == ""
        assert deleted_user.archived_at is not None
        assert deleted_user.created_at is not None
        assert deleted_user.archived_at > deleted_user.created_at

        res = client.delete(
            f"/v1/users/{user_id}", headers=headers(user_id), content_type=JSON
        )
        assert res.status_code == status.HTTP_400_BAD_REQUEST


def test_rbac_delete_user():
    wrong_id = new_id()
    user_id = new_id()
    existing_user = User(
        id=user_id,
        username="user1",
        password="hashed_password",
        salt="random-salt",
        created_at=datetime.utcnow(),
    )
    with TestEnvironment(items=[existing_user]) as client:
        res = client.delete(
            f"/v1/users/{user_id}", headers=headers(wrong_id), content_type=JSON
        )
        assert res.status_code == status.HTTP_403_FORBIDDEN

        res = client.delete(
            f"/v1/users/{user_id}",
            headers=headers(wrong_id, role="ADMIN"),
            content_type=JSON,
        )
        assert res.status_code == status.HTTP_200_OK
        deleted_user = user_repo.find(user_id)
        assert deleted_user is not None
        assert deleted_user.username == f"archived-{user_id}"
        assert deleted_user.archived
        assert deleted_user.password == ""
        assert deleted_user.salt == ""
        assert deleted_user.archived_at is not None
        assert deleted_user.created_at is not None
        assert deleted_user.archived_at > deleted_user.created_at
