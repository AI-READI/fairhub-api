import uuid
from ..db import db


class StudyContact(db.Model):
    """A study is a collection of datasets and participants"""

    def __init__(self, study):
        self.id = str(uuid.uuid4())
        self.study = study

    __tablename__ = "study_contact"

    id = db.Column(db.CHAR(36), primary_key=True)
    first_name = db.Column(db.String, nullable=False)
    last_name = db.Column(db.String, nullable=False)
    affiliation = db.Column(db.String, nullable=False)
    role = db.Column(db.String, nullable=True)
    phone = db.Column(db.String, nullable=False)
    phone_ext = db.Column(db.String, nullable=False)
    email_address = db.Column(db.String, nullable=False)
    central_contact = db.Column(db.BOOLEAN, nullable=False)

    study_id = db.Column(db.CHAR(36), db.ForeignKey("study.id"))
    study = db.relationship("Study", back_populates="study_contact")

    def to_dict(self):
        """Converts the study to a dictionary"""
        return {
            "id": self.id,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "affiliation": self.affiliation,
            "role": self.role,
            "phone": self.phone,
            "phone_ext": self.phone_ext,
            "email_address": self.email_address,
            "central_contact": self.central_contact,
        }

    @staticmethod
    def from_data(study, data: dict):
        """Creates a new study from a dictionary"""
        study_contact = StudyContact(study)
        study_contact.update(data)

        return study_contact

    def update(self, data):
        """Updates the study from a dictionary"""
        self.first_name = data["first_name"]
        self.last_name = data["last_name"]
        self.affiliation = data["affiliation"]
        self.role = data["role"]
        self.phone = data["phone"]
        self.phone_ext = data["phone_ext"]
        self.email_address = data["email_address"]
        self.central_contact = data["central_contact"]

    def validate(self):
        """Validates the lead_sponsor_last_name study"""
        violations = []
        return violations
