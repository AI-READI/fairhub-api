import uuid
from ..db import db
from sqlalchemy import String
from sqlalchemy.dialects.postgresql import ARRAY


class StudySponsorsCollaborators(db.Model):
    """A study is a collection of datasets and participants"""

    def __init__(self, study):
        self.id = str(uuid.uuid4())
        self.study = study

    __tablename__ = "study_sponsors_collaborators"

    id = db.Column(db.CHAR(36), primary_key=True)
    responsible_party_type = db.Column(db.String, nullable=False)
    responsible_party_investigator_name = db.Column(db.String, nullable=False)
    responsible_party_investigator_title = db.Column(db.String, nullable=False)
    responsible_party_investigator_affiliation = db.Column(db.String, nullable=False)
    lead_sponsor_name = db.Column(db.String, nullable=False)
    collaborator_name = db.Column(ARRAY(String), nullable=False)

    study_id = db.Column(db.CHAR(36), db.ForeignKey("study.id"))
    study = db.relationship("Study", back_populates="study_sponsors_collaborators")

    def to_dict(self):
        """Converts the study to a dictionary"""
        return {
            "id": self.id,
            "responsible_party_type": self.responsible_party_type,
            "responsible_party_investigator_name": self.responsible_party_investigator_name,
            "responsible_party_investigator_title": self.responsible_party_investigator_title,
            "responsible_party_investigator_affiliation": self.responsible_party_investigator_affiliation,
            "lead_sponsor_name": self.lead_sponsor_name,
        }

    @staticmethod
    def from_data(study, data: dict):
        """Creates a new study from a dictionary"""
        study_sponsors_collaborators = StudySponsorsCollaborators(study)
        study_sponsors_collaborators.update(data)

        return study_sponsors_collaborators

    def update(self, data):
        """Updates the study from a dictionary"""
        self.responsible_party_type = data["responsible_party_type"]

        self.responsible_party_investigator_name = data[
            "responsible_party_investigator_name"
        ]
        self.responsible_party_investigator_title = data[
            "responsible_party_investigator_title"
        ]
        self.responsible_party_investigator_affiliation = data[
            "responsible_party_investigator_affiliation"
        ]
        self.lead_sponsor_name = data["lead_sponsor_name"]
        self.collaborator_name = data["collaborator_name"]

    @staticmethod
    def from_data_(study, data: dict):
        """Creates a new study from a dictionary"""
        study_sponsors_collaborators = StudySponsorsCollaborators(study)
        study_sponsors_collaborators.update(data)

        return study_sponsors_collaborators

    def update_collaborators(self, data):
        """Updates the study from a dictionary"""
        self.collaborator_name = data["collaborator_name"]

    def validate(self):
        """Validates the lead_sponsor_last_name study"""
        violations = []
        return violations
