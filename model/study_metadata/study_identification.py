import uuid
from ..db import db


class StudyIdentification(db.Model):
    """A study is a collection of datasets and participants"""

    def __init__(self):
        self.id = str(uuid.uuid4())

    __tablename__ = "study_identification"

    id = db.Column(db.CHAR(36), primary_key=True)
    identifier = db.Column(db.String, nullable=False)
    identifier_type = db.Column(db.String, nullable=False)
    identifier_domain = db.Column(db.String, nullable=False)
    identifier_link = db.Column(db.String, nullable=False)
    secondary = db.Column(db.BOOLEAN, nullable=False)

    study_id = db.Column(db.CHAR(36), db.ForeignKey("study.id"))
    study = db.relationship("Study", back_populates="study_identification")

    def to_dict(self):
        """Converts the study to a dictionary"""
        return {
            "id": self.id,
            "identifier": self.identifier,
            "identifier_type": self.identifier_type,
            "identifier_domain": self.identifier_domain,
            "identifier_link": self.identifier_link,
            "secondary": self.secondary,
        }

    @staticmethod
    def from_data(data: dict):
        """Creates a new study from a dictionary"""
        study_identification = StudyIdentification()
        study_identification.update(data)

        return study_identification

    def update(self, data):
        """Updates the study from a dictionary"""
        self.identifier = data["identifier"]
        self.identifier_type = data["identifier_type"]
        self.identifier_domain = data["identifier_domain"]
        self.identifier_link = data["identifier_link"]
        self.secondary = data["secondary"]

    def validate(self):
        """Validates the lead_sponsor_last_name study"""
        violations = []
        return violations
