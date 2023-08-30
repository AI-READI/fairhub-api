import uuid
from datetime import datetime
from flask import jsonify

import model

from .db import db


class Study(db.Model):
    """A study is a collection of datasets and participants"""

    def __init__(self):
        self.id = str(uuid.uuid4())
        # self.created_at = datetime.now()

    __tablename__ = "study"

    id = db.Column(db.CHAR(36), primary_key=True)
    title = db.Column(db.String, nullable=False)
    image = db.Column(db.String, nullable=False)
    created_at = db.Column(db.DateTime, nullable=False)
    updated_on = db.Column(db.DateTime, nullable=False)

    dataset = db.relationship("Dataset", back_populates="study")
    study_contributors = db.relationship("StudyContributor", back_populates="study")
    participants = db.relationship("Participant", back_populates="study")
    invited_contributors = db.relationship(
        "StudyInvitedContributor", back_populates="study"
    )

    study_arm = db.relationship("StudyArm", back_populates="study")
    study_available_ipd = db.relationship("StudyAvailableIpd", back_populates="study")
    study_contact = db.relationship("StudyContact", back_populates="study")
    study_description = db.relationship(
        "StudyDescription", uselist=False, back_populates="study"
    )
    study_design = db.relationship("StudyDesign", back_populates="study")
    study_eligibility = db.relationship("StudyEligibility", back_populates="study")
    study_identification = db.relationship(
        "StudyIdentification", back_populates="study"
    )
    study_intervention = db.relationship("StudyIntervention", back_populates="study")
    study_ipdsharing = db.relationship("StudyIpdsharing", back_populates="study")
    study_link = db.relationship("StudyLink", back_populates="study")
    study_location = db.relationship("StudyLocation", back_populates="study")
    study_other = db.relationship("StudyOther", uselist=False, back_populates="study")
    study_overall_official = db.relationship(
        "StudyOverallOfficial", back_populates="study"
    )
    study_reference = db.relationship("StudyReference", back_populates="study")
    study_sponsors_collaborators = db.relationship(
        "StudySponsorsCollaborators", back_populates="study"
    )
    study_status = db.relationship("StudyStatus", back_populates="study")

    def to_dict(self):
        """Converts the study to a dictionary"""
        return {
            "id": self.id,
            "title": self.title,
            "image": self.image,
            "created_at": str(self.created_at),
            "updated_on": str(self.updated_on),
            # "study_contributors": self.study_contributors.to_dict(),
            "size": self.study_other.size if self.study_other else None,
            "description": self.study_description.brief_summary
            if self.study_description
            else None,
        }

    @staticmethod
    def from_data(data: dict):
        """Creates a new study from a dictionary"""
        study = Study()
        study.update(data)

        return study

    def update(self, data):
        """Updates the study from a dictionary"""
        self.title = data["title"]
        self.image = data["image"]
        # self.user = model.User.from_data(data["user"])
        self.updated_on = data["updated_on"]

    def validate(self):
        """Validates the study"""
        violations = []
        # if self.description.trim() == "":
        #     violations.push("A description is required")
        # if self.keywords.length < 1:
        #     violations.push("At least one keyword must be specified")
        return violations
