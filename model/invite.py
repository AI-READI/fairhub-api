import datetime
import random
import uuid

from sqlalchemy import UniqueConstraint

from .db import db

# from datetime import datetime, timezone


class Invite(db.Model):  # type: ignore
    def __init__(self, study, user, email_address: str, permission):
        self.id = str(uuid.uuid4())
        self.study = study
        self.user = user
        self.permission = permission
        self.invited_on = datetime.datetime.now(datetime.timezone.utc).timestamp()
        self.email_address = email_address
        self.created_at = datetime.datetime.now(datetime.timezone.utc).timestamp()
        self.token = random.randint(10 ** (7 - 1), (10**7) - 1)
        self.info = ""
    __tablename__ = "invite"
    id = db.Column(db.CHAR(36), primary_key=True)

    email_address = db.Column(db.String, nullable=False)
    permission = db.Column(db.String, nullable=True)
    invited_on = db.Column(db.BigInteger, nullable=False)
    token = db.Column(db.String, nullable=False)
    created_at = db.Column(db.BigInteger, nullable=False)
    info = db.Column(db.String, nullable=True)

    study_id = db.Column(
        db.CHAR(36), db.ForeignKey("study.id", ondelete="CASCADE"), nullable=True
    )
    study = db.relationship("Study", back_populates="invited_contributors")
    user_id = db.Column(db.CHAR(36), db.ForeignKey("user.id", ondelete="CASCADE"), nullable=False)
    user = db.relationship("User", back_populates="invited_contributors")

    _table_args_ = (UniqueConstraint("study_id", "email_address", name="study_per_user"))

    def to_dict(self):
        return {
            "id": self.email_address,
            "status": "invited",
            "role": self.permission,
            "email_address": self.email_address,
            "token": self.token,
            "info": self.info,
            "user_id": self.user_id
        }
