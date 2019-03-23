# Standard library
from datetime import datetime

# Internal modules
from app import db


class User(db.Model):  # type: ignore
    id: str = db.Column(db.String(50), primary_key=True)
    username: str = db.Column(db.String(100), unique=True, nullable=False)
    password: str = db.Column(db.String(100), nullable=False)
    salt: str = db.Column(db.String(100), nullable=False)
    role: str = db.Column(db.String(20), nullable=False, default="USER")
    archived: bool = db.Column(db.Boolean, nullable=False, default=False)
    created_at: datetime = db.Column(
        db.DateTime, nullable=False, default=datetime.utcnow
    )
    archived_at: datetime = db.Column(db.DateTime, nullable=True)

    def __repr__(self) -> str:
        return (
            f"User(id={self.id} username={self.username} "
            f"archived={self.archived} created_at={self.created_at} "
            f"archived_at={self.archived_at})"
        )
