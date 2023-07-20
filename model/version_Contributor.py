from sqlalchemy import String
from sqlalchemy.dialects.postgresql import ARRAY

from .db import db


class VersionContributor(db.Model):
    __tablename__ = "version_contributor"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    affiliations = db.Column(ARRAY(String), nullable=False)
    email = db.Column(db.String, nullable=False)
    firstname = db.Column(db.String, nullable=False)
    lastname = db.Column(db.String, nullable=False)
    ORCID = db.Column(db.String, nullable=False)
    roles = db.Column(ARRAY(String), nullable=False)
    status = db.Column(db.String, nullable=False)

    datasetVersion_id = db.Column(db.Integer, db.ForeignKey("datasetVersion.id"))
    datasetVersion = db.relationship(
        "DatasetVersion", back_populates="versionContributors"
    )

    def to_dict(self):
        return {
            "id": self.id,
            "affiliations": self.affiliations,
            "email": self.email,
            "firstname": self.firstname,
            "lastname": self.lastname,
            "ORCID": self.ORCID,
            "roles": self.roles,
            "status": self.status,
        }

    @staticmethod
    def from_data(data):
        versionContributor = VersionContributor()
        # versionContributor.id = data["id"]
        versionContributor.affiliations = data["affiliations"]
        versionContributor.email = data["email"]
        versionContributor.firstname = data["firstname"]
        versionContributor.lastname = data["lastname"]
        versionContributor.ORCID = data["ORCID"]
        versionContributor.roles = data["roles"]
        versionContributor.status = data["status"]
        return versionContributor
