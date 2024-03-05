import datetime
import uuid
from datetime import timezone

from model import Study

from ..db import db


class StudyCentralContact(db.Model):  # type: ignore
    """A study is a collection of datasets and participants"""

    def __init__(self, study: Study):
        self.id = str(uuid.uuid4())
        self.study = study
        self.created_at = datetime.datetime.now(timezone.utc).timestamp()

    __tablename__ = "study_contact"

    id = db.Column(db.CHAR(36), primary_key=True)
    first_name = db.Column(db.String, nullable=False)
    last_name = db.Column(db.String, nullable=False)
    degree = db.Column(db.String, nullable=False)
    identifier = db.Column(db.String, nullable=False)
    identifier_scheme = db.Column(db.String, nullable=False)
    identifier_scheme_uri = db.Column(db.String, nullable=False)
    affiliation = db.Column(db.String, nullable=False)
    affiliation_identifier = db.Column(db.String, nullable=False)
    affiliation_identifier_scheme = db.Column(db.String, nullable=False)
    affiliation_identifier_scheme_uri = db.Column(db.String, nullable=False)
    phone = db.Column(db.String, nullable=False)
    phone_ext = db.Column(db.String, nullable=False)
    email_address = db.Column(db.String, nullable=False)

    created_at = db.Column(db.BigInteger, nullable=False)

    study_id = db.Column(
        db.CHAR(36), db.ForeignKey("study.id", ondelete="CASCADE"), nullable=False
    )
    study = db.relationship("Study", back_populates="study_contact")

    def to_dict(self):
        """Converts the study to a dictionary"""
        return {
            "id": self.id,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "degree": self.degree,
            "identifier": self.identifier,
            "identifier_scheme": self.identifier_scheme,
            "identifier_scheme_uri": self.identifier_scheme_uri,
            "affiliation": self.affiliation,
            "affiliation_identifier": self.affiliation_identifier,
            "affiliation_identifier_scheme": self.affiliation_identifier_scheme,
            "affiliation_identifier_scheme_uri": self.affiliation_identifier_scheme_uri,
            "phone": self.phone,
            "phone_ext": self.phone_ext,
            "email_address": self.email_address,
            "created_at": self.created_at,
        }

    def to_dict_metadata(self):
        """Converts the study metadata to a dictionary"""
        return {
            "id": self.id,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "affiliation": self.affiliation,
            "phone": self.phone,
            "email_address": self.email_address,
        }

    @staticmethod
    def from_data(study: Study, data: dict):
        """Creates a new study from a dictionary"""
        study_contact = StudyCentralContact(study)
        study_contact.update(data)

        return study_contact

    def update(self, data: dict):
        """Updates the study from a dictionary"""
        self.first_name = data["first_name"]
        self.last_name = data["last_name"]
        self.degree = data["degree"]
        self.identifier = data["identifier"]
        self.identifier_scheme = data["identifier_scheme"]
        self.identifier_scheme_uri = data["identifier_scheme_uri"]
        self.affiliation = data["affiliation"]
        self.affiliation_identifier = data["affiliation_identifier"]
        self.affiliation_identifier_scheme = data["affiliation_identifier_scheme"]
        self.affiliation_identifier_scheme_uri = data["affiliation_identifier_scheme_uri"]
        self.phone = data["phone"]
        self.phone_ext = data["phone_ext"]
        self.email_address = data["email_address"]
        self.study.touch()

    def validate(self):
        """Validates the lead_sponsor_last_name study"""
        violations: list = []
        return violations
