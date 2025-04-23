import datetime
import uuid
from datetime import timezone

from model import Study

from ..db import db


class StudyCollaborators(db.Model):  # type: ignore
    """A study is a collection of datasets and participants"""

    def __init__(self, study):
        self.id = str(uuid.uuid4())
        self.study = study
        self.created_at = datetime.datetime.now(timezone.utc).timestamp()

    __tablename__ = "study_collaborators"

    id = db.Column(db.CHAR(36), primary_key=True)
    name = db.Column(db.String, nullable=False)
    identifier = db.Column(db.String, nullable=False)
    scheme = db.Column(db.String, nullable=False)
    scheme_uri = db.Column(db.String, nullable=False)
    created_at = db.Column(db.BigInteger, nullable=False)

    study_id = db.Column(
        db.CHAR(36),
        db.ForeignKey("study.id", ondelete="CASCADE"),
        nullable=False,
    )
    study = db.relationship("Study", back_populates="study_collaborators")

    def to_dict(self):
        """Converts the study to a dictionary"""
        return {
            "id": self.id,
            "name": self.name,
            "identifier": self.identifier,
            "identifier_scheme": self.scheme,
            "identifier_scheme_uri": self.scheme_uri,
            "created_at": self.created_at,
        }

    def to_dict_metadata(self):
        """Converts the study metadata to a dictionary"""
        return {
            "name": self.name,
        }

    def to_dict_validation(self):
        return {
            "name": self.name,
            "identifier": self.identifier,
            "identifier_scheme": {
                "value": self.identifier_scheme,
                "parent": self.identifier,
            },
        }

    def validate(self):
        data = self.to_dict_validation()
        invalid_keys = []
        for key, value in data.items():
            if isinstance(value, dict):
                if value["parent"] is not None and (
                    not isinstance(value, str) or value.strip() != ""
                ):
                    continue  # skip to next loop
            if (isinstance(value, str) and value.strip() == "") or (
                isinstance(value, list) and len(value) == 0
            ):
                invalid_keys.append({"identifier": "team", "name": key})
        return invalid_keys

    @staticmethod
    def from_data(study: Study, data: dict):
        """Creates a new study from a dictionary"""
        study_keywords = StudyCollaborators(study)
        study_keywords.update(data)

        return study_keywords

    def update(self, data: dict):
        """Updates the study from a dictionary"""
        self.name = data["name"]
        self.identifier = data["identifier"]
        self.scheme = data["identifier_scheme"]
        self.scheme_uri = data["identifier_scheme_uri"]
        self.study.touch()
