import uuid

from sqlalchemy import String
from sqlalchemy.dialects.postgresql import ARRAY

from .db import db


class InvitedStudyContributor(db.Model):
    def __init__(self):
        self.id = str(uuid.uuid4())

    __tablename__ = "invited_study_contributor"
    email_address = db.Column(String, nullable=False)
    permission = db.Column(db.String, nullable=False)
    invited_on = db.Column(db.DateTime, nullable=False)

    study_id = db.Column(db.CHAR(36), db.ForeignKey("study.id"), primary_key=True)
    study = db.relationship("Study")

    def to_dict(self):
        return {
            "email_address": self.id,
            "permission": self.affiliations,
            "date": self.email,
            "invited_on": self.first_name,
            "orcid": self.ORCID,

        }

    @staticmethod
    def from_data(data: dict):
        version_contributor = InvitedStudyContributor()
        version_contributor.affiliations = data["affiliations"]
        version_contributor.email = data["email"]
        version_contributor.first_name = data["first_name"]
        version_contributor.last_name = data["last_name"]
        version_contributor.orcid = data["orcid"]
        return version_contributor
