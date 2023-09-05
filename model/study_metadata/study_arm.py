import uuid
from sqlalchemy import String
from sqlalchemy.dialects.postgresql import ARRAY

from ..db import db


class StudyArm(db.Model):
    """A study is a collection of datasets and participants"""

    def __init__(self, study):
        self.id = str(uuid.uuid4())
        self.study = study

    __tablename__ = "study_arm"

    id = db.Column(db.CHAR(36), primary_key=True)
    label = db.Column(db.String, nullable=False)
    type = db.Column(db.String, nullable=False)
    description = db.Column(db.String, nullable=False)
    intervention_list = db.Column(ARRAY(String), nullable=False)

    study_id = db.Column(db.CHAR(36), db.ForeignKey("study.id"))
    study = db.relationship("Study", back_populates="study_arm")

    def to_dict(self):
        """Converts the study to a dictionary"""
        return {
            "id": self.id,
            "label": self.label,
            "type": self.type,
            "description": str(self.description),
            "intervention_list": self.intervention_list
           },



    @staticmethod
    def from_data(study, data):
        """Creates a new study from a dictionary"""
        study_arm = StudyArm(study)
        study_arm.update(data)
        return study_arm

    def update(self, data):
        """Updates the study from a dictionary"""
        self.label = data["label"]
        self.type = data["type"]
        self.description = data["description"]
        self.intervention_list = data["intervention_list"]

    def validate(self):
        """Validates the study"""
        violations = []
        return violations
