import uuid
from ..db import db


class StudyLink(db.Model):
    """A study is a collection of datasets and participants"""

    def __init__(self):
        self.id = str(uuid.uuid4())

    __tablename__ = "study_link"

    id = db.Column(db.CHAR(36), primary_key=True)
    url = db.Column(db.String, nullable=False)
    title = db.Column(db.String, nullable=False)

    study_id = db.Column(db.CHAR(36), db.ForeignKey("study.id"))
    study = db.relationship("Study", back_populates="study_link")

    def to_dict(self):
        """Converts the study to a dictionary"""
        return {"id": self.id, "url": self.url, "title": self.title}

    @staticmethod
    def from_data(data: dict):
        """Creates a new study from a dictionary"""
        study_link = StudyLink()
        study_link.update(data)

        return study_link

    def update(self, data):
        """Updates the study from a dictionary"""
        self.url = data["url"]
        self.title = data["title"]

    def validate(self):
        """Validates the lead_sponsor_last_name study"""
        violations = []
        return violations
