import uuid
from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Any, Dict, List

from sqlalchemy_json import NestedMutableJson

from model import Study

from .db import db


@dataclass
class StudyDashboard(db.Model):  # type: ignore
    """
    A Project Dashboard is associated with a
    REDCap Project, which is part of a study
    """

    __tablename__: str = "study_dashboard"
    # Columns
    id: str = db.Column(db.CHAR(36), primary_key=True)
    name: str = db.Column(db.String, nullable=True)
    modules: list[dict[str, (str | bool | int)]] = db.Column(
        NestedMutableJson, nullable=True
    )
    reports: list[dict[str, str]] = db.Column(NestedMutableJson, nullable=True)
    created_at: float = db.Column(db.BigInteger, nullable=False)
    updated_on: float = db.Column(db.BigInteger, nullable=False)
    # Foreign Keys
    study_id: str = db.Column(
        db.CHAR(36),
        db.ForeignKey("study.id", ondelete="CASCADE"),
        nullable=False,
    )
    redcap_id: int = db.Column(
        db.CHAR(36),
        db.ForeignKey("study_redcap.id", ondelete="CASCADE"),
        nullable=False,
    )
    # project_id: int = db.Column(
    #     db.BigInteger,
    #     db.ForeignKey("study_redcap.api_pid", ondelete="CASCADE"),
    #     nullable=True
    # )
    # Relations
    study = db.relationship(
        "Study", back_populates="study_dashboard", cascade="all, delete"
    )
    study_redcap = db.relationship(
        "StudyRedcap",
        backref="study_dashboard",
        cascade="all, delete",
    )

    def __init__(self, study: Study):
        self.study = study
        self.id = str(uuid.uuid4())
        self.created_at = datetime.now(timezone.utc).timestamp()

    def to_dict(self) -> Dict:
        """Converts the study to a dictionary"""
        return {
            "id": self.id,
            "name": self.name,
            "modules": self.modules,
            "redcap_id": self.redcap_id,
            "reports": self.reports,
            "created_at": self.created_at,
            "updated_on": self.updated_on,
        }

    @staticmethod
    def from_data(study: Study, data: Dict) -> Any:
        """Creates a new study from a dictionary"""
        study_dashboard = StudyDashboard(study)
        study_dashboard.update(data)
        return study_dashboard

    def update(self, data: Dict) -> Any:
        """Updates the study from a dictionary"""
        user_updatable_props = [
            "name",
            "modules",
            "redcap_id",
            "reports",
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
