import uuid

from ..db import db


class StudyReference(db.Model):
    """A study is a collection of datasets and participants"""

    def __init__(self):
        self.id = str(uuid.uuid4())
    __tablename__ = "study_reference"

    id = db.Column(db.CHAR(36), primary_key=True)
    identifier = db.Column(db.String, nullable=False)
    title = db.Column(db.String, nullable=False)
    type = db.Column(db.Boolean, nullable=False)
    citation = db.Column(db.String, nullable=False)

    study_id = db.Column(db.CHAR(36), db.ForeignKey("study.id"))
    study = db.relationship("Study", back_populates="study_reference")

    def to_dict(self):
        """Converts the study to a dictionary"""
        return {
            "id": self.id,
            "identifier": self.identifier,
            "title": self.title,
            "type": self.type,
            "citation": self.citation,
        }

    @staticmethod
    def from_data(data: dict):
        """Creates a new study from a dictionary"""
        study_reference = StudyReference()
        study_reference.update(data)

        return study_reference

    def update(self, data):
        """Updates the study from a dictionary"""
        self.identifier = data["identifier"]
        self.title = data["title"]
        self.type = data["type"]
        self.citation = data["citation"]


    def validate(self):
        """Validates the study"""
        violations = []
        return violations
