from sqlalchemy import String
from sqlalchemy.dialects.postgresql import ARRAY

from model import Study

from ..db import db


class StudyEligibility(db.Model):  # type: ignore
    """A study is a collection of datasets and participants"""

    def __init__(self, study: Study):
        self.study = study
        self.gender = None
        self.gender_based = None
        self.gender_description = ""
        self.minimum_age_value = None  # 18
        self.maximum_age_value = None  # 60
        self.minimum_age_unit = None
        self.maximum_age_unit = None
        self.healthy_volunteers = None
        self.inclusion_criteria = []
        self.exclusion_criteria = []
        self.study_population = ""
        self.sampling_method = None

    __tablename__ = "study_eligibility"

    gender = db.Column(db.String, nullable=True)
    gender_based = db.Column(db.String, nullable=True)
    gender_description = db.Column(db.String, nullable=False)
    minimum_age_value = db.Column(db.Integer, nullable=True)
    maximum_age_value = db.Column(db.Integer, nullable=True)
    minimum_age_unit = db.Column(db.String, nullable=True)
    maximum_age_unit = db.Column(db.String, nullable=True)
    healthy_volunteers = db.Column(db.String, nullable=True)
    inclusion_criteria = db.Column(ARRAY(String), nullable=False)
    exclusion_criteria = db.Column(ARRAY(String), nullable=False)
    study_population = db.Column(db.String, nullable=False)
    sampling_method = db.Column(db.String, nullable=True)

    study_id = db.Column(
        db.CHAR(36), db.ForeignKey("study.id", ondelete="CASCADE"), primary_key=True, nullable=False
    )
    study = db.relationship("Study", back_populates="study_eligibility")

    def to_dict(self):
        """Converts the study to a dictionary"""
        return {
            "gender": self.gender,
            "gender_based": self.gender_based,
            "gender_description": self.gender_description,
            "minimum_age_unit": self.minimum_age_unit,
            "maximum_age_unit": self.maximum_age_unit,
            "minimum_age_value": self.minimum_age_value,
            "maximum_age_value": self.maximum_age_value,
            "healthy_volunteers": self.healthy_volunteers,
            "inclusion_criteria": self.inclusion_criteria,
            "exclusion_criteria": self.exclusion_criteria,
            "study_population": self.study_population,
            "sampling_method": self.sampling_method,
            "study_type": self.study.study_design.study_type
            if self.study.study_design
            else None,
        }

    @staticmethod
    def from_data(study: Study, data: dict):
        """Creates a new study from a dictionary"""
        study_eligibility = StudyEligibility(study)
        study_eligibility.update(data)

        return study_eligibility

    def update(self, data: dict):
        """Updates the study from a dictionary"""
        self.gender = data["gender"]
        self.gender_based = data["gender_based"]
        self.gender_description = data["gender_description"]
        self.minimum_age_value = data["minimum_age_value"]
        self.minimum_age_unit = data["minimum_age_unit"]
        self.maximum_age_unit = data["maximum_age_unit"]
        self.maximum_age_value = data["maximum_age_value"]
        self.healthy_volunteers = data["healthy_volunteers"]
        self.inclusion_criteria = data["inclusion_criteria"]
        self.exclusion_criteria = data["exclusion_criteria"]
        self.study_population = data["study_population"]
        self.sampling_method = data["sampling_method"]
        self.study.touch()

    def validate(self):
        """Validates the lead_sponsor_last_name study"""
        violations: list = []
        return violations
