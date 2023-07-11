from . import db
from sqlalchemy import String
from sqlalchemy.dialects.postgresql import ARRAY


class StudyContributor(db.Model):
    __tablename__ = "study_contributor"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    affiliations = db.Column(ARRAY(String), nullable=False)
    email = db.Column(db.String, nullable=False)
    firstname = db.Column(db.String, nullable=False)
    lastname = db.Column(db.String, nullable=False)
    ORCID = db.Column(db.String, nullable=False)
    roles = db.Column(ARRAY(String), nullable=False)
    permission = db.Column(db.String, nullable=False)
    status = db.Column(db.String, nullable=False)

    study_id = db.Column(db.Integer, db.ForeignKey("study.id"))
    study = db.relationship("Study", back_populates="contributors")

    def to_dict(self):
        return {
            "id": self.id,
            "affiliations": self.affiliations,
            "email": self.email,
            "firstname": self.firstname,
            "lastname": self.lastname,
            "ORCID": self.ORCID,
            "roles": self.roles,
            "permission": self.permission,
            "status": self.status,
        }
