import uuid
from datetime import datetime
from .db import db
import datetime
from datetime import timezone


class StudyInvitedContributor(db.Model):
    def __init__(self, study, email_address, permission):
        self.id = str(uuid.uuid4())
        self.study = study
        self.permission = permission
        self.invited_on = datetime.datetime.now(timezone.utc).timestamp()
        self.email_address = email_address

    __tablename__ = "invited_study_contributor"
    email_address = db.Column(db.String, nullable=False, primary_key=True)
    permission = db.Column(db.String, nullable=False)
    invited_on = db.Column(db.BigInteger, nullable=False)

    study_id = db.Column(db.CHAR(36), db.ForeignKey("study.id"), primary_key=True)
    study = db.relationship("Study", back_populates="invited_contributors")

    def to_dict(self):
        return {
            "study_id": self.study.id,
            "email_address": self.email_address,
            "permission": self.permission,
            "invited_on": self.invited_on,
        }
