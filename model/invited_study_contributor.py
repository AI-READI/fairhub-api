import datetime
import uuid

import model

from .db import db

# from datetime import datetime, timezone


class StudyInvitedContributor(db.Model):  # type: ignore
    def __init__(self, study: model.Study, email_address: str, permission):
        self.id = str(uuid.uuid4())
        self.study = study
        self.permission = permission
        self.invited_on = datetime.datetime.now(datetime.timezone.utc).timestamp()
        self.email_address = email_address
        self.created_at = datetime.datetime.now(datetime.timezone.utc).timestamp()
        self.token = ""

    __tablename__ = "invited_study_contributor"
    email_address = db.Column(db.String, nullable=False, primary_key=True)
    permission = db.Column(db.String, nullable=False)
    invited_on = db.Column(db.BigInteger, nullable=False)
    token = db.Column(db.String, nullable=True)
    created_at = db.Column(db.BigInteger, nullable=False)

    study_id = db.Column(
        db.CHAR(36), db.ForeignKey("study.id", ondelete="CASCADE"), primary_key=True
    )
    study = db.relationship("Study", back_populates="invited_contributors")

    def to_dict(self):
        return {
            "id": self.email_address,
            "status": "invited",
            "role": self.permission,
            "email_address": self.email_address,
        }
