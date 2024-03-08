import datetime
import uuid
from datetime import timezone

from model import Study

from ..db import db


class StudyKeywords(db.Model):  # type: ignore
    """A study is a collection of datasets and participants"""

    def __init__(self, study):
        self.id = str(uuid.uuid4())
        self.study = study
        self.created_at = datetime.datetime.now(timezone.utc).timestamp()

    __tablename__ = "study_keywords"

    id = db.Column(db.CHAR(36), primary_key=True)
    name = db.Column(db.String, nullable=False)
    classification_code = db.Column(db.String, nullable=False)
    scheme = db.Column(db.String, nullable=False)
    scheme_uri = db.Column(db.String, nullable=False)
    keyword_uri = db.Column(db.String, nullable=False)
    created_at = db.Column(db.String, nullable=False)

    study_id = db.Column(
        db.CHAR(36),
        db.ForeignKey("study.id", ondelete="CASCADE"),
        nullable=False,
    )
    study = db.relationship("Study", back_populates="study_keywords")

    def to_dict(self):
        """Converts the study to a dictionary"""
        return {
            "id": self.id,
            "name": self.name,
            "classification_code": self.classification_code,
            "scheme": self.scheme,
            "scheme_uri": self.scheme_uri,
            "keyword_uri": self.keyword_uri,
            "created_at": self.created_at,
        }

    def to_dict_metadata(self):
        """Converts the study metadata to a dictionary"""
        return {
            "name": self.name,
        }

    @staticmethod
    def from_data(study: Study, data: dict):
        """Creates a new study from a dictionary"""
        study_keywords = StudyKeywords(study)
        study_keywords.update(data)

        return study_keywords

    def update(self, data: dict):
        """Updates the study from a dictionary"""
        self.name = data["name"]
        self.classification_code = data["classification_code"]
        self.scheme = data["scheme"]
        self.scheme_uri = data["scheme_uri"]
        self.keyword_uri = data["keyword_uri"]
        self.study.touch()

    def validate(self):
        """Validates the study"""
        violations: list = []
        return violations
