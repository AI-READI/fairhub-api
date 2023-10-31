import uuid
from datetime import datetime, timezone

from sqlalchemy import String
from sqlalchemy.dialects.postgresql import ARRAY

from model import Study, StudyRedcapProjectApi

from .db import db
from .study import Study


class StudyRedcapProjectDashboard(db.Model):  # type: ignore
    """A study is a collection of datasets and participants"""

    def __init__(self, study):
        self.study = study
        self.id = str(uuid.uuid4())
        self.created_at = datetime.now(timezone.utc).timestamp()

    __tablename__ = "study_redcap_project_dashboard"
    dashboard_id = db.Column(db.CHAR(36), primary_key=True)
    dashboard_name = db.Column(db.String, nullable=False)
    dashboard_modules = db.Column(ARRAY(String), nullable=False)
    created_at = db.Column(db.BigInteger, nullable=False)
    updated_on = db.Column(db.BigInteger, nullable=False)

    study_id = db.Column(
        db.CHAR(36),
        db.ForeignKey("study.id", ondelete="CASCADE"),
        nullable=False,
    )
    project_id = db.Column(
        db.CHAR(5),
        db.ForeignKey("study_redcap_project_api.project_id", ondelete="CASCADE"),
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

    def to_dict(self):
        """Converts the study to a dictionary"""
        return {
            "project_id": self.project_id,
            "dashboard_id": self.dashboard_id,
            "dashboard_name": self.dashboard_name,
            "dashboard_endpoint": self.dashboard_endpoint,
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
        self.dashboard_id = data["dashboard_id"]
        self.dashboard_name = data["dashboard_name"]
        self.dashboard_endpoint = data["dashboard_endpoint"]
        self.updated_on = datetime.now(timezone.utc).timestamp()

    def validate(self):
        """Validates the study"""
        violations: list = []
        return violations
