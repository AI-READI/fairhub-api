import datetime
import uuid
from datetime import timezone

from sqlalchemy import String
from sqlalchemy.dialects.postgresql import ARRAY

from model import Study

from ..db import db


class StudyIntervention(db.Model):  # type: ignore
    """A study is a collection of datasets and participants"""

    def __init__(self, study):
        self.id = str(uuid.uuid4())
        self.study = study
        self.created_at = datetime.datetime.now(timezone.utc).timestamp()

    __tablename__ = "study_intervention"

    id = db.Column(db.CHAR(36), primary_key=True)
    type = db.Column(db.String, nullable=True)
    name = db.Column(db.String, nullable=False)
    description = db.Column(db.String, nullable=False)
    other_name_list = db.Column(ARRAY(String), nullable=False)
    created_at = db.Column(db.BigInteger, nullable=False)

    study_id = db.Column(
        db.CHAR(36), db.ForeignKey("study.id", ondelete="CASCADE"), nullable=False
    )
    study = db.relationship("Study", back_populates="study_intervention")

    def to_dict(self):
        """Converts the study to a dictionary"""
        return {
            "id": self.id,
            "type": self.type,
            "name": self.name,
            "description": self.description,
            "other_name_list": self.other_name_list,
            "created_at": self.created_at,
        }

    def to_dict_metadata(self):
        """Converts the study metadata to a dictionary"""
        return {
            "id": self.id,
            "type": self.type,
            "name": self.name,
        }

    @staticmethod
    def from_data(study: Study, data: dict):
        """Creates a new study from a dictionary"""
        study_intervention = StudyIntervention(study)
        study_intervention.update(data)

        return study_intervention

    def update(self, data: dict):
        """Updates the study from a dictionary"""
        self.type = data["type"]
        self.name = data["name"]
        self.description = data["description"]
        self.other_name_list = data["other_name_list"]
        self.study.touch()

    def validate(self):
        """Validates the lead_sponsor_last_name study"""
        violations: list = []
        return violations
