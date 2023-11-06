import uuid
from dataclasses import dataclass
from datetime import datetime, timezone

from model import Study

from .db import db


@dataclass
class StudyRedcapProjectApi(db.Model):  # type: ignore
    """
    A REDCap Project API is associated a study
    """

    study_id: str
    project_id: int
    project_title: str
    project_api_url: str
    project_api_key: str
    project_api_active: bool
    created_at: int
    updated_on: int

    __tablename__: str = "study_redcap_project_api"
    project_id: int = db.Column(db.BigInteger, primary_key=True)
    project_title: str = db.Column(db.String, nullable=False)
    project_api_url: str = db.Column(db.String, nullable=False)
    project_api_key: str = db.Column(db.String, nullable=False)
    project_api_active: bool = db.Column(db.Boolean, nullable=False)
    created_at: int = db.Column(db.BigInteger, nullable=False)
    updated_on: int = db.Column(db.BigInteger, nullable=False)

    study_id: str = db.Column(
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

    def __init__(self, study):
        self.study = study
        self.id = str(uuid.uuid4())
        self.created_at = datetime.now(timezone.utc).timestamp()

    def to_dict(self):
        """Converts the study to a dictionary"""
        return {
            "project_id": self.project_id,
            "project_title": self.project_title,
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
        return self

    def validate(self):
        """Validates the study"""
        violations: list = []
        return violations
