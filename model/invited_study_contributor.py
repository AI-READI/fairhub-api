import uuid

from sqlalchemy import String
from sqlalchemy.dialects.postgresql import ARRAY

from .db import db


class InvitedStudyContributor(db.Model):
    def __init__(self):
        self.id = str(uuid.uuid4())

    __tablename__ = "invited_study_contributor"
    email_address = db.Column(ARRAY(String), nullable=False)
    permission = db.Column(db.String, nullable=False)
    date = db.Column(db.String, nullable=False)
    last_name = db.Column(db.String, nullable=False)

    study_id = db.Column(db.CHAR(36), db.ForeignKey("study.id"))
    study = db.relationship("Study")

    def to_dict(self):
        return {
            "id": self.id,
            "affiliations": self.affiliations,
            "email": self.email,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "orcid": self.ORCID,
            "roles": self.roles,
            "status": self.status,
        }

    @staticmethod
    def from_data(data: dict):
        version_contributor = InvitedStudyContributor()
        version_contributor.affiliations = data["affiliations"]
        version_contributor.email = data["email"]
        version_contributor.first_name = data["first_name"]
        version_contributor.last_name = data["last_name"]
        version_contributor.orcid = data["orcid"]
        version_contributor.roles = data["roles"]
        version_contributor.status = data["status"]
        return version_contributor
