from __main__ import db
from sqlalchemy import String
from sqlalchemy.dialects.postgresql import ARRAY


class StudyContributor(db.Model):
    __tablename__ = "study_contributor"
    id = db.Column(db.Integer, primary_key=True)
    affiliations = db.Column(ARRAY(String), nullable=False)
    email = db.Column(db.String)
    firstname = db.Column(db.String)
    lastname = db.Column(db.String)
    ORCID = db.Column(db.String)
    roles = db.Column(ARRAY(String), nullable=False)
    permission = db.Column(db.String)
    status = db.Column(db.String)

    study_id = db.Column(db.Integer, db.ForeignKey("study.id"))
    study = db.relationship("Study", back_populates="contributors")
