import uuid
from datetime import datetime, timezone

from model import Study

from .db import db


class StudyRedcapProjectApi(db.Model):  # type: ignore
    """A study is a collection of datasets and participants"""

    def __init__(self, study):
        self.study = study
        self.id = str(uuid.uuid4())
        self.created_at = datetime.now(timezone.utc).timestamp()

    __tablename__ = "study_redcap_project_api"
    project_id = db.Column(db.CHAR(5), primary_key=True)
    project_title = db.Column(db.String, nullable=False)
    project_api_url = db.Column(db.String, nullable=False)
    project_api_key = db.Column(db.String, nullable=False)
    project_api_active = db.Column(db.Boolean, nullable=False)
    created_at = db.Column(db.BigInteger, nullable=False)
    updated_on = db.Column(db.BigInteger, nullable=False)

    study_id = db.Column(
        db.CHAR(36),
        db.ForeignKey("study.id", ondelete="CASCADE"),
        nullable=False,
    )
    study = db.relationship(
        "Study", back_populates="study_redcap_project_apis", cascade="all, delete"
    )
    study_redcap_project_dashboards = db.relationship(
        "StudyRedcapProjectDashboard", back_populates="study_redcap_project_api"
    )

    def to_dict(self):
        """Converts the study to a dictionary"""
        return {
            "study_id": self.study.id,
            "project_title": self.project_title,
            "project_id": self.project_id,
            "project_api_url": self.project_api_url,
            "project_api_key": self.project_api_key,
            "project_api_active": self.project_api_active,
        }

    @staticmethod
    def from_data(study: Study, data: dict):
        """Creates a new study from a dictionary"""
        study_redcap_project_api = StudyRedcapProjectApi(study)
        study_redcap_project_api.update(data)
        return study_redcap_project_api

    def update(self, data: dict):
        """Updates the study from a dictionary"""
        assignable = {key for key in self.to_dict().keys() if key.startswith("project")}
        for key, val in data.items():
            if key in assignable:
                setattr(self, key, val)
        self.updated_on = datetime.now(timezone.utc).timestamp()

    def validate(self):
        """Validates the study"""
        violations: list = []
        return violations
