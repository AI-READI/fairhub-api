import datetime
import re
from typing import cast
import uuid

from flask import g

import model
from apis import exception

from .db import db


class StudyException(Exception):
    pass


class Study(db.Model):  # type: ignore
    """A study is a collection of datasets and participants"""

    def __init__(self):
        self.id = str(uuid.uuid4())
        self.created_at = datetime.datetime.now(datetime.timezone.utc).timestamp()

        self.study_status = model.StudyStatus(self)
        self.study_sponsors = model.StudySponsors(self)
        self.study_design = model.StudyDesign(self)
        self.study_eligibility = model.StudyEligibility(self)
        self.study_description = model.StudyDescription(self)
        self.study_other = model.StudyOther(self)
        self.study_oversight = model.StudyOversight(self)

    __tablename__ = "study"
    id = db.Column(db.CHAR(36), primary_key=True)

    title = db.Column(db.String(300), nullable=False)
    image = db.Column(db.String, nullable=False)
    short_description = db.Column(db.String(300), nullable=False)

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
    study_sponsors = db.relationship(
        "StudySponsors",
        uselist=False,
        back_populates="study",
        cascade="all, delete",
    )
    study_central_contact = db.relationship(
        "StudyCentralContact",
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
    # NOTE: Has not been tested
    study_redcap = db.relationship(
        "StudyRedcap", back_populates="study", cascade="all, delete"
    )
    # NOTE: Has not been tested
    study_dashboard = db.relationship(
        "StudyDashboard", back_populates="study", cascade="all, delete"
    )
    study_intervention = db.relationship(
        "StudyIntervention",
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
    study_keywords = db.relationship(
        "StudyKeywords",
        back_populates="study",
        cascade="all, delete",
    )
    study_conditions = db.relationship(
        "StudyConditions",
        back_populates="study",
        cascade="all, delete",
    )
    study_collaborators = db.relationship(
        "StudyCollaborators",
        back_populates="study",
        cascade="all, delete",
    )
    study_oversight = db.relationship(
        "StudyOversight",
        uselist=False,
        back_populates="study",
        cascade="all, delete",
    )
    study_overall_official = db.relationship(
        "StudyOverallOfficial",
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

        return {
            "id": self.id,
            "title": self.title,
            "short_description": self.short_description,
            "image": self.image,
            "created_at": self.created_at,
            "updated_on": self.updated_on,
            "size": self.study_other.size if self.study_other else None,
            "description": (
                self.study_description.brief_summary if self.study_description else None
            ),
            "owner": owner.to_dict()["id"] if owner else None,
            "role": contributor_permission.to_dict()["role"]
            if contributor_permission
            else None,
        }

    def to_dict_study_metadata(self):
        # self.study_contact: Iterable = []
        primary = [
            i.to_dict_metadata()
            for i in self.study_identification  # type: ignore
            if not i.secondary
        ]

        return {
            "arms": [i.to_dict_metadata() for i in self.study_arm],  # type: ignore
            "central_contacts": [
                i.to_dict_metadata() for i in self.study_central_contact  # type: ignore
            ],
            "description": self.study_description.to_dict_metadata(),
            "design": self.study_design.to_dict(),
            "eligibility": self.study_eligibility.to_dict_metadata(),
            "primary_identifier": primary[0] if len(primary) else None,
            "secondary_identifiers": [
                i.to_dict_metadata()
                for i in self.study_identification  # type: ignore
                if i.secondary
            ],
            "interventions": [
                i.to_dict_metadata() for i in self.study_intervention  # type: ignore
            ],
            "locations": [
                i.to_dict_metadata() for i in self.study_location  # type: ignore
            ],
            "overall_officials": [
                i.to_dict_metadata()
                for i in self.study_overall_official  # type: ignore
            ],
            "sponsors": self.study_sponsors.to_dict_metadata(),
            "collaborators": [
                i.to_dict_metadata() for i in self.study_collaborators  # type: ignore
            ],
            "status": self.study_status.to_dict_metadata(),
            "oversight": self.study_oversight.to_dict(),
            "conditions": [
                i.to_dict_metadata() for i in self.study_conditions  # type: ignore
            ],
            "keywords": [
                i.to_dict_metadata() for i in self.study_keywords  # type: ignore
            ],
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

        self.title = data["title"]
        self.short_description = data["short_description"]
        if "image" in data and data["image"]:
            self.image = data["image"]
        self.updated_on = datetime.datetime.now(datetime.timezone.utc).timestamp()

    def update_identification_id(self, data):
        clinical_id = None
        identifiers = [
            i for i in cast(list, self.study_identification)
            if re.match(r"^NCT\d{8}$", i.identifier)
        ]
        if not identifiers:
            clinical_id = model.StudyIdentification(self, False)
            self.study_identification.append(clinical_id)
            model.db.session.add(clinical_id)
        else:
            clinical_id = identifiers[0]

        if clinical_id is not None:
            clinical_id.updating_from_integration(data)

    def import_from_clinical_data(self, data):
        """Updates the study from a dictionary"""

        self.study_description.updating_from_integration(data)
        self.study_status.updating_from_integration(data)
        self.study_eligibility.updating_from_integration(data)
        self.study_sponsors.updating_from_integration(data)
        self.study_design.updating_from_integration(data)
        self.study_oversight.updating_from_integration(data)

        interventions_data = data.get("armsInterventionsModule", {}).get(
            "interventions", []
        )
        # Loop through an array and delete each object
        for intervention in cast(list, self.study_intervention):
            model.db.session.delete(intervention)

        for intervention_dict in interventions_data:
            # Make the new intervention
            intervention = model.StudyIntervention(self)
            # Put data from dict into it
            intervention.updating_from_integration(intervention_dict)
            # Add to a database
            self.study_intervention.append(intervention)

        collaborators_data = data.get("sponsorCollaboratorsModule", {}).get(
            "collaborators", []
        )
        # Loop through an array and delete each object
        for collaborator in cast(list, self.study_collaborators):
            model.db.session.delete(collaborator)

        for collaborator_dict in collaborators_data:
            # Make the new intervention
            collaborator = model.StudyCollaborators(self)
            # Put data from dict into it
            collaborator.updating_from_integration(collaborator_dict)
            # Add to a database
            self.study_collaborators.append(collaborator)

        arms_data = data.get("armsInterventionsModule", {}).get("armGroups", [])
        # Loop through an array and delete each object
        for arm in cast(list, self.study_arm):
            model.db.session.delete(arm)

        for arm_dict in arms_data:
            # Make the new intervention
            arm = model.StudyArm(self)
            # Put data from dict into it
            arm.updating_from_integration(arm_dict)
            # Add to a database
            self.study_arm.append(arm)

        overall_official_data = data.get("contactsLocationsModule", {}).get(
            "overallOfficials", []
        )
        # Loop through an array and delete each object
        for oo in cast(list, self.study_overall_official):
            model.db.session.delete(oo)

        for oo_dict in overall_official_data:
            # Make the new intervention
            o_o = model.StudyOverallOfficial(self)
            # Put data from dict into it
            o_o.updating_from_integration(oo_dict)
            # Add to a database
            self.study_overall_official.append(o_o)

        location_data = data.get("contactsLocationsModule", {}).get("locations", [])
        # Loop through an array and delete each object
        for location in cast(list, self.study_location):
            model.db.session.delete(location)

        for location_dict in location_data:
            # Make the new intervention
            location = model.StudyLocation(self)
            # Put data from dict into it
            location.updating_from_integration(location_dict)
            # Add to a database
            self.study_location.append(location)

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
