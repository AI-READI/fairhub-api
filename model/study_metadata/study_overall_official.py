import datetime
import uuid
from datetime import timezone

from model import Study

from ..db import db


class StudyOverallOfficial(db.Model):  # type: ignore
    """A study is a collection of datasets and participants"""

    def __init__(self, study):
        self.id = str(uuid.uuid4())
        self.study = study
        self.created_at = datetime.datetime.now(timezone.utc).timestamp()
        self.degree = ""
        self.identifier = ""
        self.identifier_scheme = ""
        self.identifier_scheme_uri = ""
        self.affiliation_identifier = ""
        self.affiliation_identifier_scheme = ""
        self.affiliation_identifier_scheme_uri = ""

    __tablename__ = "study_overall_official"

    id = db.Column(db.CHAR(36), primary_key=True)
    name = db.Column(db.String, nullable=False)
    degree = db.Column(db.String, nullable=False)
    identifier = db.Column(db.String, nullable=False)
    identifier_scheme = db.Column(db.String, nullable=False)
    identifier_scheme_uri = db.Column(db.String, nullable=False)
    affiliation = db.Column(db.String, nullable=False)
    affiliation_identifier = db.Column(db.String, nullable=False)
    affiliation_identifier_scheme = db.Column(db.String, nullable=False)
    affiliation_identifier_scheme_uri = db.Column(db.String, nullable=False)
    role = db.Column(db.String, nullable=True)

    created_at = db.Column(db.BigInteger, nullable=False)

    study_id = db.Column(
        db.CHAR(36), db.ForeignKey("study.id", ondelete="CASCADE"), nullable=False
    )
    study = db.relationship("Study", back_populates="study_overall_official")

    def to_dict(self):
        """Converts the study to a dictionary"""
        return {
            "id": self.id,
            "name": self.name,
            "affiliation": self.affiliation,
            "role": self.role,
            "degree": self.degree,
            "identifier": self.identifier,
            "identifier_scheme": self.identifier_scheme,
            "identifier_scheme_uri": self.identifier_scheme_uri,
            "affiliation_identifier": self.affiliation_identifier,
            "affiliation_identifier_scheme": self.affiliation_identifier_scheme,
            "affiliation_identifier_scheme_uri": self.affiliation_identifier_scheme_uri,
            "created_at": self.created_at,
        }

    def to_dict_metadata(self):
        """Converts the study metadata to a dictionary"""
        return {
            "name": self.name,
            "affiliation": self.affiliation,
            "role": self.role,
        }

    @staticmethod
    def from_data(study: Study, data: dict):
        """Creates a new study from a dictionary"""
        study_overall_official = StudyOverallOfficial(study)
        study_overall_official.update(data)

        return study_overall_official

    def update(self, data: dict):
        """Updates the study from a dictionary"""
        self.name = data["name"]
        self.affiliation = data["affiliation"]
        self.degree = data["degree"]
        self.identifier = data["identifier"]
        self.identifier_scheme = data["identifier_scheme"]
        self.identifier_scheme_uri = data["identifier_scheme_uri"]
        self.affiliation_identifier = data["affiliation_identifier"]
        self.affiliation_identifier_scheme = data["affiliation_identifier_scheme"]
        self.affiliation_identifier_scheme_uri = data[
            "affiliation_identifier_scheme_uri"
        ]
        self.role = data["role"]
        self.study.touch()

    def validate(self):
        """Validates the study"""
        violations: list = []
        return violations
