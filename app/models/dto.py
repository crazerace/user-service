# Standard library
from dataclasses import dataclass
from typing import Any, Dict

# Internal modules
from app.error import BadRequestError


@dataclass
class NewUserRequest:
    username: str
    password: str

    @classmethod
    def fromdict(cls, raw: Dict[str, Any]) -> "NewUserRequest":
        username: str = raw["username"]
        password: str = raw["password"]
        if not (isinstance(username, str) and isinstance(password, str)):
            raise BadRequestError("Incorrect field types")
        return cls(username=password, password=password)
