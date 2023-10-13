import datetime
import uuid

from flask import g

import model
from apis import exception

from .db import db

# from datetime import datetime, timezone


class StudyException(Exception):
    pass


class Study(db.Model):  # type: ignore
    """A study is a collection of datasets and participants"""

    def __init__(self):
        self.id = str(uuid.uuid4())
        self.created_at = datetime.datetime.now(datetime.timezone.utc).timestamp()
        #
        self.study_status = model.StudyStatus(self)
        self.study_sponsors_collaborators = model.StudySponsorsCollaborators(self)
        self.study_design = model.StudyDesign(self)
        self.study_eligibility = model.StudyEligibility(self)
        self.study_ipdsharing = model.StudyIpdsharing(self)
        self.study_description = model.StudyDescription(self)

        self.study_other = model.StudyOther(self)
        # self.study_contributors = model.StudyContributor(self)

    __tablename__ = "study"
    id = db.Column(db.CHAR(36), primary_key=True)
    title = db.Column(db.String, nullable=False)
    image = db.Column(db.String, nullable=False)
    created_at = db.Column(db.BigInteger, nullable=False)
    updated_on = db.Column(db.BigInteger, nullable=False)

    dataset = db.relationship(
        "Dataset",
        back_populates="study",
        cascade="all, delete",
    )
    study_contributors = db.relationship(
        "StudyContributor",
        back_populates="study",
        lazy="dynamic",
        cascade="all, delete",
    )
    participants = db.relationship(
        "Participant",
        back_populates="study",
        cascade="all, delete",
    )
    invited_contributors = db.relationship(
        "StudyInvitedContributor",
        back_populates="study",
        lazy="dynamic",
        cascade="all, delete",
    )

    study_arm = db.relationship(
        "StudyArm",
        back_populates="study",
        cascade="all, delete",
    )
    study_available_ipd = db.relationship(
        "StudyAvailableIpd",
        back_populates="study",
        cascade="all, delete",
    )
    study_contact = db.relationship(
        "StudyContact",
        back_populates="study",
        cascade="all, delete",
    )
    study_description = db.relationship(
        "StudyDescription",
        uselist=False,
        back_populates="study",
        cascade="all, delete",
    )
    study_design = db.relationship(
        "StudyDesign",
        uselist=False,
        back_populates="study",
        cascade="all, delete",
    )
    study_eligibility = db.relationship(
        "StudyEligibility",
        uselist=False,
        back_populates="study",
        cascade="all, delete",
    )
    study_identification = db.relationship(
        "StudyIdentification",
        back_populates="study",
        cascade="all, delete",
    )
    study_intervention = db.relationship(
        "StudyIntervention",
        back_populates="study",
        cascade="all, delete",
    )
    study_ipdsharing = db.relationship(
        "StudyIpdsharing",
        uselist=False,
        back_populates="study",
        cascade="all, delete",
    )
    study_link = db.relationship(
        "StudyLink",
        back_populates="study",
        cascade="all, delete",
    )
    study_location = db.relationship(
        "StudyLocation",
        back_populates="study",
        cascade="all, delete",
    )
    study_other = db.relationship(
        "StudyOther",
        uselist=False,
        back_populates="study",
        cascade="all, delete",
    )
    study_overall_official = db.relationship(
        "StudyOverallOfficial",
        back_populates="study",
        cascade="all, delete",
    )
    study_reference = db.relationship(
        "StudyReference",
        back_populates="study",
        cascade="all, delete",
    )
    study_sponsors_collaborators = db.relationship(
        "StudySponsorsCollaborators",
        uselist=False,
        back_populates="study",
        cascade="all, delete",
    )
    study_status = db.relationship(
        "StudyStatus",
        uselist=False,
        back_populates="study",
        cascade="all, delete",
    )

    def to_dict(self):
        """Converts the study to a dictionary"""
        owner = self.study_contributors.filter(
            model.StudyContributor.permission == "owner"
        ).first()
        contributor_permission = self.study_contributors.filter(
            model.StudyContributor.user_id == g.user.id
        ).first()
        print(contributor_permission)
        return {
            "id": self.id,
            "title": self.title,
            "image": self.image,
            "created_at": self.created_at,
            "updated_on": self.updated_on,
            "size": self.study_other.size if self.study_other else None,
            "description": self.study_description.brief_summary
            if self.study_description
            else None,
            "owner": owner.to_dict()["id"] if owner else None,
            "role": contributor_permission.to_dict()["role"],
        }

    @staticmethod
    def from_data(data: dict):
        """Creates a new study from a dictionary"""
        study = Study()
        study.update(data)

        return study

    def update(self, data: dict):
        """Updates the study from a dictionary"""
        if not data["title"]:
            raise exception.ValidationException("title is required")
        if not data["image"]:
            raise exception.ValidationException("image is required")

        self.title = data["title"]
        self.image = data["image"]
        self.updated_on = datetime.datetime.now(datetime.timezone.utc).timestamp()

    def validate(self):
        """Validates the study"""
        violations: list = []
        # if self.description.trim() == "":
        #     violations.push("A description is required")
        # if self.keywords.length < 1:
        #     violations.push("At least one keyword must be specified")
        return violations

    def touch(self):
        self.updated_on = datetime.datetime.now(datetime.timezone.utc).timestamp()

    def add_user_to_study(self, user, permission):
        """add user to study"""
        contributor = self.study_contributors.filter(
            model.StudyContributor.user_id == user.id
        ).all()
        if contributor:
            raise StudyException("User is already exists in study")
        contributor = model.StudyContributor(self, user, permission)
        db.session.add(contributor)
        return contributor

    def invite_user_to_study(self, email_address, permission):
        invited_contributor = self.invited_contributors.filter(
            model.StudyInvitedContributor.email_address == email_address
        ).one_or_none()
        if invited_contributor:
            raise StudyException(
                "This email address has already been invited to this study"
            )
        contributor_add = model.StudyInvitedContributor(self, email_address, permission)
        db.session.add(contributor_add)
        return contributor_add
