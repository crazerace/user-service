# Standard library
from typing import List
from uuid import uuid4

# 3rd party modules
from flask.testing import FlaskClient

# Internal modules
from app import app


JSON: str = "application/json"


def new_id() -> str:
    return str(uuid4()).lower()


"""
def insert_items(items: List[db.Model]) -> None:
    for item in get_default_data() + items:
        db.session.add(item)
    db.session.commit()
"""


class TestEnvironment:
    def __init__(self) -> None:
        self.client = app.test_client()

    def __enter__(self) -> FlaskClient:
        return self.client

    def __exit__(self, type, value, traceback) -> None:
        pass

