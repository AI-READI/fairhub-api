import uuid
from ..db import db
from datetime import timezone
import datetime


class StudyIdentification(db.Model):
    def __init__(self, study, secondary):
        self.id = str(uuid.uuid4())
        self.study = study
        self.secondary = secondary
        self.created_at = datetime.datetime.now(timezone.utc).timestamp()

    __tablename__ = "study_identification"
    id = db.Column(db.CHAR(36), primary_key=True)
    identifier = db.Column(db.String, nullable=False)
    identifier_type = db.Column(db.String, nullable=False)
    identifier_domain = db.Column(db.String, nullable=False)
    identifier_link = db.Column(db.String, nullable=False)
    secondary = db.Column(db.BOOLEAN, nullable=False)
    created_at = db.Column(db.BigInteger, nullable=False)

    study_id = db.Column(db.CHAR(36), db.ForeignKey("study.id", ondelete="CASCADE"), nullable=False)
    study = db.relationship("Study", back_populates="study_identification")

    def to_dict(self):
        return {
            "id": self.id,
            "identifier": self.identifier,
            "identifier_type": self.identifier_type,
            "identifier_domain": self.identifier_domain,
            "identifier_link": self.identifier_link,
            "created_at": self.created_at,
        }

    @staticmethod
    def from_data(study, data: dict, secondary):
        """Creates a new study from a dictionary"""
        study_identification = StudyIdentification(study, secondary)
        study_identification.update(data)

        return study_identification

    def update(self, data):
        """Updates the study from a dictionary"""
        self.identifier = data["identifier"]
        self.identifier_type = data["identifier_type"]
        self.identifier_domain = data["identifier_domain"]
        self.identifier_link = data["identifier_link"]
        self.study.touch()

    def validate(self):
        """Validates the lead_sponsor_last_name study"""
        violations = []
        return violations
