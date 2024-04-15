import datetime
from datetime import timezone

from .db import db


class EmailVerification(db.Model):  # type: ignore
    def __init__(self):
        self.created_at = datetime.datetime.now(timezone.utc).timestamp()

    __tablename__ = "email_verification"
    id = db.Column(db.CHAR(36), primary_key=True)
    token = db.Column(db.CHAR(36), nullable=False)
    created_at = db.Column(db.CHAR(36), nullable=False)

    user_id = db.Column(db.CHAR(36), db.ForeignKey("user.id"), nullable=False)
    user = db.relationship("User", back_populates="email_verification")

    def to_dict(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "token": self.token,
            "created_at": self.created_at,
        }
