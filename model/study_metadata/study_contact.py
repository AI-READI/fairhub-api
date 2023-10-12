import datetime
import uuid
from datetime import timezone

from model import Study

from ..db import db


class StudyContact(db.Model):
    """A study is a collection of datasets and participants"""

    def __init__(self, study: Study, role, central_contact):
        self.id = str(uuid.uuid4())
        self.study = study
        self.role = role
        self.central_contact = central_contact
        self.created_at = datetime.datetime.now(timezone.utc).timestamp()

    __tablename__ = "study_contact"

    id = db.Column(db.CHAR(36), primary_key=True)
    name = db.Column(db.String, nullable=False)
    affiliation = db.Column(db.String, nullable=False)
    role = db.Column(db.String, nullable=True)
    phone = db.Column(db.String, nullable=False)
    phone_ext = db.Column(db.String, nullable=False)
    email_address = db.Column(db.String, nullable=False)
    central_contact = db.Column(db.BOOLEAN, nullable=False)
    created_at = db.Column(db.BigInteger, nullable=False)

    study_id = db.Column(
        db.CHAR(36), db.ForeignKey("study.id", ondelete="CASCADE"), nullable=False
    )
    study = db.relationship("Study", back_populates="study_contact")

    def to_dict(self):
        """Converts the study to a dictionary"""
        return {
            "id": self.id,
            "name": self.name,
            "affiliation": self.affiliation,
            "role": self.role,
            "phone": self.phone,
            "phone_ext": self.phone_ext,
            "email_address": self.email_address,
            "central_contact": self.central_contact,
            "created_at": self.created_at,
        }

    @staticmethod
    def from_data(study: Study, data: dict, role, central_contact):
        """Creates a new study from a dictionary"""
        study_contact = StudyContact(study, role, central_contact)
        study_contact.update(data)

        return study_contact

    def update(self, data: dict):
        """Updates the study from a dictionary"""
        self.name = data["name"]
        self.affiliation = data["affiliation"]
        # self.role = data["role"]
        self.phone = data["phone"]
        self.phone_ext = data["phone_ext"]
        self.email_address = data["email_address"]
        self.study.touch()

    def validate(self):
        """Validates the lead_sponsor_last_name study"""
        violations = []
        return violations
