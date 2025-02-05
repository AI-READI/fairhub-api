from . import User

from .db import db


class Session(db.Model):  # type: ignore
    def __init__(self, id, user: User):  # pylint: disable=redefined-builtin
        self.id = id
        self.user = user

    __tablename__ = "session"
    id = db.Column(db.CHAR(36), primary_key=True)
    expires_at = db.Column(db.BigInteger, nullable=False)

    user_id = db.Column(db.CHAR(36), db.ForeignKey("user.id"), nullable=False)

    user = db.relationship(
        "User",
        back_populates="session",
    )

    def to_dict(self):
        return {
            "id": self.id,
            "expires_at": self.expires_at,
            "user_id": self.user_id,
        }

    @staticmethod
    def from_data(id, expires_at, user: User):  # pylint: disable=redefined-builtin
        session = Session(id, user)
        session.update(expires_at)
        return session

    def update(self, expires_at):
        self.expires_at = expires_at
