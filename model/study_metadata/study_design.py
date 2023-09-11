import uuid
from sqlalchemy import String
from sqlalchemy.dialects.postgresql import ARRAY

from ..db import db


class StudyDesign(db.Model):
    """A study is a collection of datasets and participants"""

    def __init__(self, study):
        self.id = str(uuid.uuid4())
        self.study = study

        self.design_allocation = ""
        self.study_type = ""
        self.design_intervention_model = ""
        self.design_intervention_model_description = ""
        self.design_primary_purpose = ""
        self.design_masking = ""
        self.design_masking_description = ""
        self.design_who_masked_list = []
        self.phase_list = []
        self.enrollment_count = 0
        self.enrollment_type = ""
        self.number_arms = 0
        self.design_observational_model_list = []
        self.design_time_perspective_list = []
        self.bio_spec_retention = ""
        self.bio_spec_description = ""
        self.target_duration = ""
        self.number_groups_cohorts = 0

    __tablename__ = "study_design"

    id = db.Column(db.CHAR(36), primary_key=True)
    design_allocation = db.Column(db.String, nullable=True)
    study_type = db.Column(db.String, nullable=False)
    design_intervention_model = db.Column(db.String, nullable=True)
    design_intervention_model_description = db.Column(db.String, nullable=True)
    design_primary_purpose = db.Column(db.String, nullable=True)
    design_masking = db.Column(db.String, nullable=True)
    design_masking_description = db.Column(db.String, nullable=True)
    design_who_masked_list = db.Column(ARRAY(String), nullable=True)
    phase_list = db.Column(ARRAY(String), nullable=True)
    enrollment_count = db.Column(db.Integer, nullable=False)
    enrollment_type = db.Column(db.String, nullable=False)
    number_arms = db.Column(db.Integer, nullable=True)
    design_observational_model_list = db.Column(ARRAY(String), nullable=True)
    design_time_perspective_list = db.Column(ARRAY(String), nullable=True)
    bio_spec_retention = db.Column(db.String, nullable=True)
    bio_spec_description = db.Column(db.String, nullable=True)
    target_duration = db.Column(db.String, nullable=True)
    number_groups_cohorts = db.Column(db.Integer, nullable=True)

    study_id = db.Column(db.CHAR(36), db.ForeignKey("study.id"), nullable=True)
    study = db.relationship("Study", back_populates="study_design")

    def to_dict(self):
        """Converts the study to a dictionary"""
        return {
            "id": self.id,
            "design_allocation": self.design_allocation,
            "study_type": self.study_type,
            "design_intervention_model": self.design_intervention_model,
            "design_intervention_model_description": self.design_intervention_model_description,
            "design_primary_purpose": self.design_primary_purpose,
            "design_masking": self.design_masking,
            "design_masking_description": self.design_masking_description,
            "design_who_masked_list": self.design_who_masked_list,
            "phase_list": self.phase_list,
            "enrollment_count": self.enrollment_count,
            "enrollment_type": self.enrollment_type,
            "number_arms": self.number_arms,
            "design_observational_model_list": self.design_observational_model_list,
            "design_time_perspective_list": self.design_time_perspective_list,
            "bio_spec_retention": self.bio_spec_retention,
            "bio_spec_description": self.bio_spec_description,
            "target_duration": self.target_duration,
            "number_groups_cohorts": self.number_groups_cohorts,
        }

    @staticmethod
    def from_data(study, data: dict):
        """Creates a new study from a dictionary"""
        study_design = StudyDesign(study)
        study_design.update(data)

        return study_design

    def update(self, data):
        """Updates the study from a dictionary"""
        self.design_allocation = data["design_allocation"]
        self.study_type = data["study_type"]
        self.design_intervention_model = data["design_intervention_model"]
        self.design_intervention_model_description = data[
            "design_intervention_model_description"
        ]
        self.design_primary_purpose = data["design_primary_purpose"]
        self.design_masking = data["design_masking"]
        self.design_masking_description = data["design_masking_description"]
        self.design_who_masked_list = data["design_who_masked_list"]
        self.phase_list = data["phase_list"]
        self.enrollment_count = data["enrollment_count"]
        self.enrollment_type = data["enrollment_type"]
        self.number_arms = data["number_arms"]
        self.design_observational_model_list = data["design_observational_model_list"]
        self.design_time_perspective_list = data["design_time_perspective_list"]
        self.bio_spec_retention = data["bio_spec_retention"]
        self.bio_spec_description = data["bio_spec_description"]
        self.target_duration = data["target_duration"]
        self.number_groups_cohorts = data["number_groups_cohorts"]
        self.study.touch()

    def validate(self):
        """Validates the study"""
        violations = []
        return violations
