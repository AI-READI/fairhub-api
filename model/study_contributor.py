from sqlalchemy import String
from sqlalchemy.dialects.postgresql import ARRAY
import uuid
from .db import db


class StudyContributor(db.Model):
    def __init__(self):
        self.id = str(uuid.uuid4())

    __tablename__ = "study_contributor"
    id = db.Column(db.CHAR(36), primary_key=True)
    affiliations = db.Column(ARRAY(String), nullable=False)
    email = db.Column(db.String, nullable=False)
    first_name = db.Column(db.String, nullable=False)
    last_name = db.Column(db.String, nullable=False)
    orcid = db.Column(db.String, nullable=False)
    roles = db.Column(ARRAY(String), nullable=False)
    permission = db.Column(db.String, nullable=False)
    status = db.Column(db.String, nullable=False)

    study_id = db.Column(db.CHAR(36), db.ForeignKey("study.id"))
    study = db.relationship("Study", back_populates="contributors")

    def to_dict(self):
        return {
            "id": self.id,
            "affiliations": self.affiliations,
            "email": self.email,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "orcid": self.orcid,
            "roles": self.roles,
            "permission": self.permission,
            "status": self.status,
        }

    @staticmethod
    def from_data(data):
        study_contributor = StudyContributor()
        # for i in data.values():
        #     print(i)
        # study_contributor.id = data["id"]
        study_contributor.affiliations = data["affiliations"]
        study_contributor.email = data["email"]
        study_contributor.first_name = data["first_name"]
        study_contributor.last_name = data["last_name"]
        study_contributor.orcid = data["orcid"]
        study_contributor.roles = data["roles"]
        study_contributor.permission = data["permission"]
        study_contributor.status = data["status"]
        return study_contributor
