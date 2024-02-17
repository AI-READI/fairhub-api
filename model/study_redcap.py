import uuid
from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Any, Dict, List

from model import Study

from .db import db


@dataclass
class StudyRedcap(db.Model):  # type: ignore
    """
    A REDCap Project API is associated a study
    """

    __tablename__: str = "study_redcap"
    # Columns
    id: str = db.Column(db.CHAR(36), primary_key=True)
    title: str = db.Column(db.String, nullable=True)
    api_pid: int = db.Column(db.BigInteger, nullable=True)
    api_url: str = db.Column(db.String, nullable=True)
    api_key: str = db.Column(db.String, nullable=True)
    api_active: bool = db.Column(db.Boolean, nullable=True)
    created_at: float = db.Column(db.BigInteger, nullable=False)
    updated_on: float = db.Column(db.BigInteger, nullable=False)
    # Foreign Keys
    study_id: str = db.Column(
        db.CHAR(36),
        db.ForeignKey("study.id", ondelete="CASCADE"),
        nullable=False,
    )
    # Relations
    study = db.relationship(
        "Study", back_populates="study_redcap", cascade="all, delete"
    )

    def __init__(self, study):
        self.study = study
        self.id = str(uuid.uuid4())
        self.created_at = datetime.now(timezone.utc).timestamp()

    def to_dict(self) -> Dict:
        """Converts the study to a dictionary"""
        return {
            "id": self.id,
            "title": self.title,
            "api_pid": self.api_pid,
            "api_url": self.api_url,
            "api_key": self.api_key,
            "api_active": self.api_active,
        }

    @staticmethod
    def from_data(study: Study, data: Dict) -> Any:
        """Creates a new study from a dictionary"""
        study_redcap = StudyRedcap(study)
        study_redcap.update(data)
        return study_redcap

    def update(self, data: Dict) -> Any:
        """Updates the study from a dictionary"""
        user_updatable_props = [
            "title",
            "api_pid",
            "api_url",
            "api_key",
            "api_active",
        ]
        for key, val in data.items():
            if key in user_updatable_props:
                setattr(self, key, val)
        self.updated_on = datetime.now(timezone.utc).timestamp()
        return self

    def validate(self) -> List:
        """Validates the study"""
        violations: list = []
        return violations
