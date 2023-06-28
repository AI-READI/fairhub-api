
from sqlalchemy import String
from __main__ import db
from sqlalchemy.dialects.postgresql import ARRAY


class VersionContributor(db.Model):
    __tablename__ = 'version_contributor'
    id = db.Column(db.Integer, primary_key=True)
    affiliations = db.Column(ARRAY(String), nullable=False)
    email = db.Column(db.String)
    firstname = db.Column(db.String)
    lastname = db.Column(db.String)
    ORCID = db.Column(db.String)
    roles = db.Column(ARRAY(String), nullable=False)
    status = db.Column(db.String)

    datasetVersion_id = db.Column(db.Integer, db.ForeignKey("datasetVersion.id"))
    datasetVersion = db.relationship("VersionContributor", back_populates="datasetVersion")