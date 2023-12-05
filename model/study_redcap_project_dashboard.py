import uuid
from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Any, Dict, List

from sqlalchemy_json import NestedMutableJson

from model import Study

from .db import db


@dataclass
class StudyRedcapProjectDashboard(db.Model):  # type: ignore
    """
    A Project Dashboard is associated with a
    REDCap Project, which is part of a study
    """

    __tablename__: str = "study_redcap_project_dashboard"
    dashboard_id: str = db.Column(db.CHAR(36), primary_key=True)
    dashboard_name: str = db.Column(db.String, nullable=False)
    dashboard_modules: list[dict[str, (str | bool | int)]] = db.Column(
        NestedMutableJson, nullable=True
    )
    reports: list[dict[str, str]] = db.Column(NestedMutableJson, nullable=True)
    created_at: float = db.Column(db.BigInteger, nullable=False)
    updated_on: float = db.Column(db.BigInteger, nullable=False)
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

    def to_dict(self) -> Dict:
        """Converts the study to a dictionary"""
        return {
            "project_id": self.project_id,
            "dashboard_id": self.dashboard_id,
            "dashboard_name": self.dashboard_name,
            "dashboard_modules": self.dashboard_modules,
            "reports": self.reports,
            "created_at": self.created_at,
            "updated_on": self.updated_on,
        }

    @staticmethod
    def from_data(study: Study, data: Dict) -> Any:
        """Creates a new study from a dictionary"""
        study_redcap_project_dashboard = StudyRedcapProjectDashboard(study)
        study_redcap_project_dashboard.update(data)
        return study_redcap_project_dashboard

    def update(self, data: Dict) -> Any:
        """Updates the study from a dictionary"""
        user_updatable_props = [
            "project_id",
            "dashboard_id",
            "dashboard_name",
            "dashboard_modules",
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
