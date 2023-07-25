from sqlalchemy import String
from sqlalchemy.dialects.postgresql import ARRAY
import uuid
from .db import db


class VersionContributor(db.Model):
    def __init__(self):
        self.id = str(uuid.uuid4())

    __tablename__ = "version_contributor"
    id = db.Column(db.CHAR(36), primary_key=True)
    affiliations = db.Column(ARRAY(String), nullable=False)
    email = db.Column(db.String, nullable=False)
    first_name = db.Column(db.String, nullable=False)
    last_name = db.Column(db.String, nullable=False)
    orcid = db.Column(db.String, nullable=False)
    roles = db.Column(ARRAY(String), nullable=False)
    status = db.Column(db.String, nullable=False)

    dataset_version_id = db.Column(db.CHAR(36), db.ForeignKey("dataset_version.id"))
    dataset_version = db.relationship(
        "DatasetVersion", back_populates="versionContributors"
    )

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
    def from_data(data):
        version_contributor = VersionContributor()
        # versionContributor.id = data["id"]
        version_contributor.affiliations = data["affiliations"]
        version_contributor.email = data["email"]
        version_contributor.first_name = data["first_name"]
        version_contributor.last_name = data["last_name"]
        version_contributor.orcid = data["orcid"]
        version_contributor.roles = data["roles"]
        version_contributor.status = data["status"]
        return version_contributor
