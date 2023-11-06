import uuid
from dataclasses import dataclass
from datetime import datetime, timezone

from sqlalchemy import JSON
from sqlalchemy.dialects.postgresql import ARRAY

from model import Study

from .db import db


@dataclass
class StudyRedcapProjectDashboard(db.Model):  # type: ignore
    """
    A Project Dashboard is associated with a
    REDCap Project, which is part of a study
    """

    project_id: int
    dashboard_id: str
    dashboard_name: str
    dashboard_modules: list[dict[str, (str | bool | int)]]
    created_at: int
    updated_on: int

    __tablename__: str = "study_redcap_project_dashboard"
    dashboard_id: str = db.Column(db.CHAR(36), primary_key=True)
    dashboard_name: str = db.Column(db.String, nullable=False)
    dashboard_modules: list[dict[str, (str | bool | int)]] = db.Column(
        ARRAY(JSON), nullable=True
    )
    created_at: int = db.Column(db.BigInteger, nullable=False)
    updated_on: int = db.Column(db.BigInteger, nullable=False)
    project_id: int = db.Column(
        db.BigInteger,
        db.ForeignKey("study_redcap_project_api.project_id", ondelete="CASCADE"),
        nullable=False,
    )
    study_id: str = db.Column(
        db.CHAR(36),
        db.ForeignKey("study.id", ondelete="CASCADE"),
        nullable=False,
    )
    study = db.relationship(
        "Study", back_populates="study_redcap_project_dashboards", cascade="all, delete"
    )
    study_redcap_project_api = db.relationship(
        "StudyRedcapProjectApi",
        back_populates="study_redcap_project_dashboards",
        cascade="all, delete",
    )

    def __init__(self, study):
        self.study = study
        self.dashboard_id = str(uuid.uuid4())
        self.created_at = datetime.now(timezone.utc).timestamp()

    def to_dict(self):
        """Converts the study to a dictionary"""
        return {
            "project_id": self.project_id,
            "dashboard_id": self.dashboard_id,
            "dashboard_name": self.dashboard_name,
            "dashboard_modules": self.dashboard_modules,
            "created_at": self.created_at,
            "updated_on": self.updated_on,
        }

    @staticmethod
    def from_data(study: Study, data: dict):
        """Creates a new study from a dictionary"""
        study_redcap_project_dashboard = StudyRedcapProjectDashboard(study)
        study_redcap_project_dashboard.update(data)
        return study_redcap_project_dashboard

    def update(self, data: dict):
        """Updates the study from a dictionary"""
        assignable = {
            key
            for key in self.to_dict().keys()
            if key.startswith("project") or key.startswith("dashboard")
        }
        for key, val in data.items():
            if key in assignable:
                setattr(self, key, val)
        self.updated_on = datetime.now(timezone.utc).timestamp()
        return self

    def validate(self):
        """Validates the study"""
        violations: list = []
        return violations
