# Standard library
from dataclasses import dataclass
from datetime import datetime
from typing import Any, Dict, List

# 3rd party modules
from crazerace.http.error import BadRequestError


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


@dataclass
class LoginRequest:
    username: str
    password: str

    @classmethod
    def fromdict(cls, raw: Dict[str, Any]) -> "LoginRequest":
        username: str = raw["username"]
        password: str = raw["password"]
        if not (isinstance(username, str) and isinstance(password, str)):
            raise BadRequestError("Incorrect field types")
        return cls(username=username, password=password)


@dataclass
class LoginResponse:
    user_id: str
    token: str

    def todict(self) -> Dict[str, str]:
        return {"userId": self.user_id, "token": self.token}


@dataclass
class UserDTO:
    id: str
    username: str
    created_at: datetime

    def todict(self) -> Dict[str, str]:
        return {
            "id": self.id,
            "username": self.username,
            "createdAt": f"{self.created_at}",
        }


@dataclass
class SearchResponse:
    results: List[UserDTO]

    def todict(self) -> Dict[str, List[Dict[str, str]]]:
        return {"results": [res.todict() for res in self.results]}
