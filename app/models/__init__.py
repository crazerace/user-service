# Standard library
from datetime import datetime

# Internal modules
from app import db


class User(db.Model):  # type: ignore
    id: str = db.Column(db.String(50), primary_key=True)
    username: str = db.Column(db.String(100), nullable=False)
    password: str = db.Column(db.String(100), nullable=False)
    salt: str = db.Column(db.String(100), nullable=False)
    created_at: datetime = db.Column(
        db.DateTime, nullable=False, default=datetime.utcnow
    )

    def __repr__(self) -> str:
        return (
            f"User(id={self.id} username={self.username} created_at={self.created_at})"
        )
