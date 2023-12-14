import datetime
import uuid
from datetime import timezone

from .db import db


class Notification(db.Model):  # type: ignore
    def __init__(self, user):
        self.id = str(uuid.uuid4())
        self.created_at = datetime.datetime.now(timezone.utc).timestamp()
        self.user = user

    __tablename__ = "notification"
    id = db.Column(db.CHAR(36), primary_key=True)
    title = db.Column(db.String, nullable=False)
    message = db.Column(db.String, nullable=False)
    type = db.Column(db.String, nullable=False)
    target = db.Column(db.String, nullable=False)
    read = db.Column(db.BOOLEAN, nullable=False)
    created_at = db.Column(db.BigInteger, nullable=False)

    user_id = db.Column(db.CHAR(36), db.ForeignKey("user.id"), nullable=False)
    user = db.relationship("User", back_populates="notification")

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "message": self.message,
            "type": self.type,
            "target": self.target,
            "read": self.read,
            "created_at": self.created_at,
        }

    @staticmethod
    def from_data(user, data: dict):
        notification = Notification(user)
        notification.update(data)
        return notification

    def update(self, data: dict):
        self.title = data["title"]
        self.message = data["message"]
        self.type = data["type"]
        self.target = data["target"]
        self.read = data["read"]
