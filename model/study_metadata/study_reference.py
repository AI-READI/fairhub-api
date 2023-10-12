import datetime
import uuid
from datetime import timezone

from model import Study

from ..db import db


class StudyReference(db.Model):  # type: ignore
    """A study is a collection of datasets and participants"""

    def __init__(self, study):
        self.id = str(uuid.uuid4())
        self.study = study
        self.created_at = datetime.datetime.now(timezone.utc).timestamp()

    __tablename__ = "study_reference"

    id = db.Column(db.CHAR(36), primary_key=True)
    identifier = db.Column(db.String, nullable=False)
    type = db.Column(db.String, nullable=False)
    citation = db.Column(db.String, nullable=False)
    created_at = db.Column(db.BigInteger, nullable=False)

    study_id = db.Column(
        db.CHAR(36), db.ForeignKey("study.id", ondelete="CASCADE"), nullable=False
    )
    study = db.relationship("Study", back_populates="study_reference")

    def to_dict(self):
        """Converts the study to a dictionary"""
        return {
            "id": self.id,
            "identifier": self.identifier,
            "type": self.type,
            "citation": self.citation,
            "created_at": self.created_at,
        }

    @staticmethod
    def from_data(study: Study, data: dict):
        """Creates a new study from a dictionary"""
        study_reference = StudyReference(study)
        study_reference.update(data)

        return study_reference

    def update(self, data: dict):
        """Updates the study from a dictionary"""
        self.identifier = data["identifier"]
        self.type = data["type"]
        self.citation = data["citation"]
        self.study.touch()

    def validate(self):
        """Validates the study"""
        violations: list = []
        return violations
