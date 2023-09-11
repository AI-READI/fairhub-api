import uuid
from datetime import datetime
from datetime import timezone
import model
from .db import db
import datetime


class Study(db.Model):
    """A study is a collection of datasets and participants"""

    def __init__(self):
        self.id = str(uuid.uuid4())
        self.created_at = datetime.datetime.now(timezone.utc).timestamp()
        #
        self.study_status = model.StudyStatus(self)
        self.study_sponsors_collaborators = model.StudySponsorsCollaborators(self)
        self.study_design = model.StudyDesign(self)
        self.study_eligibility = model.StudyEligibility(self)
        self.study_ipdsharing = model.StudyIpdsharing(self)
        self.study_description = model.StudyDescription(self)

        self.study_other = model.StudyOther(self)

    __tablename__ = "study"
    id = db.Column(db.CHAR(36), primary_key=True)
    title = db.Column(db.String, nullable=False)
    image = db.Column(db.String, nullable=False)
    created_at = db.Column(db.BigInteger, nullable=False)
    updated_on = db.Column(db.BigInteger, nullable=False)

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
    study_design = db.relationship("StudyDesign", uselist=False, back_populates="study")
    study_eligibility = db.relationship(
        "StudyEligibility", uselist=False, back_populates="study"
    )
    study_identification = db.relationship(
        "StudyIdentification", back_populates="study"
    )
    study_intervention = db.relationship("StudyIntervention", back_populates="study")
    study_ipdsharing = db.relationship(
        "StudyIpdsharing", uselist=False, back_populates="study"
    )
    study_link = db.relationship("StudyLink", back_populates="study")
    study_location = db.relationship("StudyLocation", back_populates="study")
    study_other = db.relationship("StudyOther", uselist=False, back_populates="study")
    study_overall_official = db.relationship(
        "StudyOverallOfficial", back_populates="study"
    )
    study_reference = db.relationship("StudyReference", back_populates="study")
    study_sponsors_collaborators = db.relationship(
        "StudySponsorsCollaborators", uselist=False, back_populates="study"
    )
    study_status = db.relationship("StudyStatus", uselist=False, back_populates="study")

    def to_dict(self):
        """Converts the study to a dictionary"""
        return {
            "id": self.id,
            "title": self.title,
            "image": self.image,
            "created_at": self.created_at,
            "updated_on": self.updated_on,
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
        self.updated_on = datetime.datetime.now(timezone.utc).timestamp()

    def validate(self):
        """Validates the study"""
        violations = []
        # if self.description.trim() == "":
        #     violations.push("A description is required")
        # if self.keywords.length < 1:
        #     violations.push("At least one keyword must be specified")
        return violations

    def touch(self):
        self.updated_on = datetime.datetime.now(timezone.utc).timestamp()
