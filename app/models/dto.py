# Standard library
from dataclasses import dataclass
from typing import Any, Dict

# Internal modules
from app.error import BadRequestError


@dataclass
class NewUserRequest:
    username: str
    password: str
    rep_password: str

    @classmethod
    def fromdict(cls, raw: Dict[str, Any]) -> "NewUserRequest":
        username: str = raw["username"]
        password: str = raw["password"]
        rep_password: str = raw["repPassword"]
        if not (
            isinstance(username, str)
            and isinstance(password, str)
            and isinstance(rep_password, str)
        ):
            raise BadRequestError("Incorrect field types")
        return cls(username=username, password=password, rep_password=rep_password)
