import uuid
from ..db import db
from sqlalchemy import String
from sqlalchemy.dialects.postgresql import ARRAY
from datetime import timezone
import datetime


class StudyIntervention(db.Model):
    """A study is a collection of datasets and participants"""

    def __init__(self, study):
        self.id = str(uuid.uuid4())
        self.study = study
        self.created_at = datetime.datetime.now(timezone.utc).timestamp()

    __tablename__ = "study_intervention"

    id = db.Column(db.CHAR(36), primary_key=True)
    type = db.Column(db.String, nullable=False)
    name = db.Column(db.String, nullable=False)
    description = db.Column(db.String, nullable=False)
    arm_group_label_list = db.Column(ARRAY(String), nullable=False)
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
            "arm_group_label_list": self.arm_group_label_list,
            "other_name_list": self.other_name_list,
            "created_at": self.created_at,
        }

    @staticmethod
    def from_data(study, data: dict):
        """Creates a new study from a dictionary"""
        study_intervention = StudyIntervention(study)
        study_intervention.update(data)

        return study_intervention

    def update(self, data):
        """Updates the study from a dictionary"""
        self.type = data["type"]
        self.name = data["name"]
        self.description = data["description"]
        self.arm_group_label_list = data["arm_group_label_list"]
        self.other_name_list = data["other_name_list"]
        self.study.touch()

    def validate(self):
        """Validates the lead_sponsor_last_name study"""
        violations = []
        return violations
