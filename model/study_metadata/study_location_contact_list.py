import datetime
import uuid
from datetime import timezone

from model import Study

from ..db import db


class StudyLocationContactList(db.Model):  # type: ignore
    """A study is a collection of datasets and participants"""

    def __init__(self, study):
        self.id = str(uuid.uuid4())
        self.study = study
        self.created_at = datetime.datetime.now(timezone.utc).timestamp()

    __tablename__ = "study_location_location_list"

    id = db.Column(db.CHAR(36), primary_key=True)
    first_name = db.Column(db.String, nullable=False)
    last_name = db.Column(db.String, nullable=False)
    identifier = db.Column(db.String, nullable=False)
    identifier_scheme = db.Column(db.String, nullable=False)
    zip = db.Column(db.String, nullable=False)
    role = db.Column(db.String, nullable=False)
    phone = db.Column(db.String, nullable=False)
    phone_ext = db.Column(db.String, nullable=False)
    email_address = db.Column(db.String, nullable=False)
    created_at = db.Column(db.BigInteger, nullable=False)

    study_location_id = db.Column(
        db.CHAR(36), db.ForeignKey("study_location.id", ondelete="CASCADE"), nullable=False
    )
    study_location = db.relationship("StudyLocation", back_populates="study_location_location_list")

    def to_dict(self):
        """Converts the study to a dictionary"""
        return {
            "id": self.id,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "identifier": self.identifier,
            "identifier_scheme": self.identifier_scheme,
            "zip": self.zip,
            "role": self.role,
            "phone": self.phone,
            "phone_ext": self.phone_ext,
            "email_address": self.email_address,
            "created_at": self.created_at,
        }

    # def to_dict_metadata(self):
    #     """Converts the study metadata to a dictionary"""
    #     return {
    #         "id": self.id,
    #         "facility": self.facility,
    #         "country": self.country,
    #     }

    @staticmethod
    def from_data(study: Study, data: dict):
        """Creates a new study from a dictionary"""
        study_location_contact_list = StudyLocationContactList(study)
        study_location_contact_list.update(data)

        return study_location_contact_list

    def update(self, data: dict):
        """Updates the study from a dictionary"""
        self.first_name = data["first_name"]
        self.last_name = data["last_name"]
        self.identifier = data["identifier"]
        self.identifier_scheme = data["identifier_scheme"]
        self.zip = data["zip"]
        self.role = data["role"]
        self.phone = data["phone"]
        self.phone_ext = data["phone_ext"]
        self.email_address = data["email_address"]
        self.study.touch()

    def validate(self):
        """Validates the lead_sponsor_last_name study"""
        violations: list = []
        return violations
