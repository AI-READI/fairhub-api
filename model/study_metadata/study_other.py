import uuid

from sqlalchemy import String
from sqlalchemy.dialects.postgresql import ARRAY

from model import Study

from ..db import db


class StudyOther(db.Model):  # type: ignore
    """A study is a collection of datasets and participants"""

    def __init__(self, study):
        self.id = str(uuid.uuid4())
        self.study = study
        self.oversight_has_dmc = False
        self.conditions = []
        self.keywords = []
        self.size = 0

    __tablename__ = "study_other"

    id = db.Column(db.CHAR(36), primary_key=True)
    oversight_has_dmc = db.Column(db.BOOLEAN, nullable=False)
    conditions = db.Column(ARRAY(String), nullable=False)
    keywords = db.Column(ARRAY(String), nullable=False)
    size = db.Column(db.BigInteger, nullable=False)

    study_id = db.Column(
        db.CHAR(36), db.ForeignKey("study.id", ondelete="CASCADE"), nullable=False
    )
    study = db.relationship("Study", back_populates="study_other")

    def to_dict(self):
        """Converts the study to a dictionary"""
        return {
            "id": self.id,
            "oversight_has_dmc": self.oversight_has_dmc,
            "conditions": self.conditions,
            "keywords": self.keywords,
            "size": self.size,
        }

    @staticmethod
    def from_data(study: Study, data: dict):
        """Creates a new study from a dictionary"""
        study_other = StudyOther(study)
        study_other.update(data)

        return study_other

    def update(self, data: dict):
        """Updates the study from a dictionary"""
        self.oversight_has_dmc = data["oversight_has_dmc"]
        self.conditions = data["conditions"]
        self.keywords = data["keywords"]
        self.size = data["size"]
        self.study.touch()

    def validate(self):
        """Validates the study"""
        violations: list = []
        return violations
