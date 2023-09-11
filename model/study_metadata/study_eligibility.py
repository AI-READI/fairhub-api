import uuid
from ..db import db
from sqlalchemy import String
from sqlalchemy.dialects.postgresql import ARRAY


class StudyEligibility(db.Model):
    """A study is a collection of datasets and participants"""

    def __init__(self, study):
        self.id = str(uuid.uuid4())
        self.study = study
        self.gender = ""
        self.gender_based = ""
        self.gender_description = ""
        self.minimum_age_value = 18
        self.maximum_age_value = 60
        self.minimum_age_unit = ""
        self.maximum_age_unit = ""
        self.healthy_volunteers = ""
        self.inclusion_criteria = []
        self.exclusion_criteria = []
        self.study_population = ""
        self.sampling_method = ""

    __tablename__ = "study_eligibility"

    id = db.Column(db.CHAR(36), primary_key=True)
    gender = db.Column(db.String, nullable=False)
    gender_based = db.Column(db.String, nullable=False)
    gender_description = db.Column(db.String, nullable=False)
    minimum_age_value = db.Column(db.Integer, nullable=False)
    maximum_age_value = db.Column(db.Integer, nullable=False)
    minimum_age_unit = db.Column(db.String, nullable=False)
    maximum_age_unit = db.Column(db.String, nullable=False)
    healthy_volunteers = db.Column(db.String, nullable=True)
    inclusion_criteria = db.Column(ARRAY(String), nullable=False)
    exclusion_criteria = db.Column(ARRAY(String), nullable=False)
    study_population = db.Column(db.String, nullable=True)
    sampling_method = db.Column(db.String, nullable=True)

    study_id = db.Column(db.CHAR(36), db.ForeignKey("study.id"))
    study = db.relationship("Study", back_populates="study_eligibility")

    def to_dict(self):
        """Converts the study to a dictionary"""
        return {
            "id": self.id,
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
    def from_data(study, data: dict):
        """Creates a new study from a dictionary"""
        study_eligibility = StudyEligibility(study)
        study_eligibility.update(data)

        return study_eligibility

    def update(self, data):
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
        violations = []
        return violations
