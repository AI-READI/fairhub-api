import uuid
from ..db import db
from datetime import timezone
import datetime


class StudyLink(db.Model):
    """A study is a collection of datasets and participants"""

    def __init__(self, study):
        self.id = str(uuid.uuid4())
        self.study = study
        self.created_at = datetime.datetime.now(timezone.utc).timestamp()

    __tablename__ = "study_link"

    id = db.Column(db.CHAR(36), primary_key=True)
    url = db.Column(db.String, nullable=False)
    title = db.Column(db.String, nullable=False)
    created_at = db.Column(db.BigInteger, nullable=False)

    study_id = db.Column(
        db.CHAR(36), db.ForeignKey("study.id", ondelete="CASCADE"), nullable=False
    )
    study = db.relationship("Study", back_populates="study_link")

    def to_dict(self):
        """Converts the study to a dictionary"""
        return {
            "id": self.id,
            "url": self.url,
            "title": self.title,
            "created_at": self.created_at,
        }

    @staticmethod
    def from_data(study, data: dict):
        """Creates a new study from a dictionary"""
        study_link = StudyLink(study)
        study_link.update(data)

        return study_link

    def update(self, data):
        """Updates the study from a dictionary"""
        self.url = data["url"]
        self.title = data["title"]
        self.study.touch()

    def validate(self):
        """Validates the lead_sponsor_last_name study"""
        violations = []
        return violations
