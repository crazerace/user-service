# Standard library
from datetime import datetime
from typing import List

# Internal modules
from app import db


class AuthEvent(db.Model):  # type: ignore
    __tablename__ = "authentication_event"
    id: int = db.Column(db.Integer, primary_key=True)
    user_id: str = db.Column(
        db.String(50), db.ForeignKey("user_account.id"), nullable=False
    )
    client_id: str = db.Column(db.String(50), nullable=False)
    ip_address: str = db.Column(db.String(50), nullable=False)
    event_type: str = db.Column(db.String(50), nullable=False)
    succeeded: bool = db.Column(db.Boolean, nullable=False, default=True)
    created_at: datetime = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def __repr__(self) -> str:
        return (
            f"AuthEvent(id={self.id}, user_id={self.user_id}, "
            f"client_id={self.client_id}, client_ip={self.client_ip}, "
            f"event_type={self.event_type}, succeeded={self.succeeded}, "
            f"created_at={self.created_at})"
        )


class RenewToken(db.Model):  # type: ignore
    __tablename__ = "renew_token"
    id: int = db.Column(db.Integer, primary_key=True)
    token: str = db.Column(db.String(100), unique=True, nullable=False)
    user_id: str = db.Column(
        db.String(50), db.ForeignKey("user_account.id"), nullable=False
    )
    used: bool = db.Column(db.Boolean, nullable=False, default=False)
    created_at: datetime = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    valid_to: datetime = db.Column(db.DateTime, nullable=False)

    def __repr__(self) -> str:
        return (
            f"RenewToken(id={self.id}, user_id={self.user_id}, "
            f"used={self.used}, created_at={self.created_at}, "
            f"valid_to={self.valid_to})"
        )


class User(db.Model):  # type: ignore
    __tablename__ = "user_account"
    id: str = db.Column(db.String(50), primary_key=True)
    username: str = db.Column(db.String(100), unique=True, nullable=False)
    password: str = db.Column(db.String(100), nullable=False)
    salt: str = db.Column(db.String(100), nullable=False)
    role: str = db.Column(db.String(20), nullable=False, default="USER")
    archived: bool = db.Column(db.Boolean, nullable=False, default=False)
    created_at: datetime = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    archived_at: datetime = db.Column(db.DateTime, nullable=True)
    auth_events: List[AuthEvent] = db.relationship(
        "AuthEvent", backref="user_account", lazy=True
    )
    renew_tokens: List[RenewToken] = db.relationship(
        "RenewToken", backref="user_account", lazy=True
    )

    def __repr__(self) -> str:
        return (
            f"User(id={self.id}, username={self.username}, "
            f"archived={self.archived}, created_at={self.created_at}, "
            f"archived_at={self.archived_at})"
        )
