from sqlalchemy import String
from sqlalchemy.dialects.postgresql import ARRAY

from model import Study

from ..db import db


class StudySponsors(db.Model):  # type: ignore
    """A study is a collection of datasets and participants"""

    def __init__(self, study):
        self.study = study
        self.responsible_party_type = None
        self.responsible_party_investigator_first_name = ""
        self.responsible_party_investigator_last_name = ""
        self.responsible_party_investigator_title = ""
        self.responsible_party_investigator_identifier_value = ""
        self.responsible_party_investigator_identifier_scheme = ""
        self.responsible_party_investigator_identifier_scheme_uri = ""
        self.responsible_party_investigator_affiliation_name = ""
        self.responsible_party_investigator_affiliation_identifier_value = ""
        self.responsible_party_investigator_affiliation_identifier_scheme = ""
        self.responsible_party_investigator_affiliation_identifier_scheme_uri = ""
        self.lead_sponsor_name = ""
        self.lead_sponsor_identifier = ""
        self.lead_sponsor_scheme = ""
        self.lead_sponsor_scheme_uri = ""

    __tablename__ = "study_sponsors"

    responsible_party_type = db.Column(db.String, nullable=True)
    responsible_party_investigator_first_name = db.Column(db.String, nullable=False)
    responsible_party_investigator_last_name = db.Column(db.String, nullable=False)
    responsible_party_investigator_title = db.Column(db.String, nullable=False)
    responsible_party_investigator_identifier_value = db.Column(
        db.String, nullable=False
    )
    responsible_party_investigator_identifier_scheme = db.Column(
        db.String, nullable=False
    )
    responsible_party_investigator_identifier_scheme_uri = db.Column(
        db.String, nullable=False
    )
    responsible_party_investigator_affiliation_name = db.Column(
        db.String, nullable=False
    )
    responsible_party_investigator_affiliation_identifier_value = db.Column(
        db.String, nullable=False
    )
    responsible_party_investigator_affiliation_identifier_scheme = db.Column(
        db.String, nullable=False
    )
    responsible_party_investigator_affiliation_identifier_scheme_uri = db.Column(
        db.String, nullable=False
    )
    lead_sponsor_name = db.Column(db.String, nullable=False)
    lead_sponsor_identifier = db.Column(db.String, nullable=False)
    lead_sponsor_scheme = db.Column(db.String, nullable=False)
    lead_sponsor_scheme_uri = db.Column(ARRAY(String), nullable=False)

    study_id = db.Column(
        db.CHAR(36),
        db.ForeignKey("study.id", ondelete="CASCADE"),
        primary_key=True,
        nullable=False,
    )
    study = db.relationship("Study", back_populates="study_sponsors")

    def to_dict(self):
        """Converts the study to a dictionary"""
        return {
            "responsible_party_type": self.responsible_party_type,
            "responsible_party_investigator_first_name": self.responsible_party_investigator_first_name,
            "responsible_party_investigator_last_name": self.responsible_party_investigator_last_name,
            "responsible_party_investigator_title": self.responsible_party_investigator_title,
            "responsible_party_investigator_identifier_value": self.responsible_party_investigator_identifier_value,
            "responsible_party_investigator_identifier_scheme": self.responsible_party_investigator_identifier_scheme,
            "responsible_party_investigator_identifier_scheme_uri": self.responsible_party_investigator_identifier_scheme_uri,  # noqa: E501
            "responsible_party_investigator_affiliation_name": self.responsible_party_investigator_affiliation_name,
            "responsible_party_investigator_affiliation_identifier_scheme": self.responsible_party_investigator_affiliation_identifier_scheme,  # noqa: E501
            "responsible_party_investigator_affiliation_identifier_value": self.responsible_party_investigator_affiliation_identifier_value,  # noqa: E501
            "responsible_party_investigator_affiliation_identifier_scheme_uri": self.responsible_party_investigator_affiliation_identifier_scheme_uri,  # noqa: E501
            "lead_sponsor_name": self.lead_sponsor_name,
            "lead_sponsor_identifier": self.lead_sponsor_identifier,
            "lead_sponsor_scheme": self.lead_sponsor_scheme,
            "lead_sponsor_scheme_uri": self.lead_sponsor_scheme_uri,
        }

    def to_dict_metadata(self):
        """Converts the study metadata to a dictionary"""
        return {
            "responsible_party_type": self.responsible_party_type,
            "responsible_party_investigator_first_name": self.responsible_party_investigator_first_name,
            "responsible_party_investigator_last_name": self.responsible_party_investigator_last_name,
            "lead_sponsor_name": self.lead_sponsor_name,
        }

    @staticmethod
    def from_data(study: Study, data: dict):
        """Creates a new study from a dictionary"""
        study_sponsors = StudySponsors(study)
        study_sponsors.update(data)

        return study_sponsors

    def update(self, data: dict):
        """Updates the study from a dictionary"""
        self.responsible_party_type = data["responsible_party_type"]
        self.responsible_party_investigator_first_name = data[
            "responsible_party_investigator_first_name"
        ]
        self.responsible_party_investigator_last_name = data[
            "responsible_party_investigator_last_name"
        ]
        self.responsible_party_investigator_title = data[
            "responsible_party_investigator_title"
        ]
        self.responsible_party_investigator_identifier_value = data[
            "responsible_party_investigator_identifier_value"
        ]
        self.responsible_party_investigator_identifier_scheme = data[
            "responsible_party_investigator_identifier_scheme"
        ]
        self.responsible_party_investigator_identifier_scheme_uri = data[
            "responsible_party_investigator_identifier_scheme_uri"
        ]
        self.responsible_party_investigator_affiliation_name = data[
            "responsible_party_investigator_affiliation_name"
        ]
        self.responsible_party_investigator_affiliation_identifier_scheme = data[
            "responsible_party_investigator_affiliation_identifier_scheme"
        ]
        self.responsible_party_investigator_affiliation_identifier_value = data[
            "responsible_party_investigator_affiliation_identifier_value"
        ]
        self.responsible_party_investigator_affiliation_identifier_scheme_uri = data[
            "responsible_party_investigator_affiliation_identifier_scheme_uri"
        ]
        self.lead_sponsor_name = data["lead_sponsor_name"]
        self.lead_sponsor_identifier = data["lead_sponsor_identifier"]
        self.lead_sponsor_scheme = data["lead_sponsor_scheme"]
        self.lead_sponsor_scheme_uri = data["lead_sponsor_scheme_uri"]

    def validate(self):
        """Validates the lead_sponsor_last_name study"""
        violations: list = []
        return violations
