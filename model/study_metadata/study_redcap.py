from model import Study

from ..db import db


class StudyRedcap(db.Model):  # type: ignore
    """A study is a collection of datasets and participants"""

    def __init__(self, study):
        self.study = study
        self.redcap_api_token = None
        self.redcap_api_url = None
        self.redcap_project_id = None
        self.redcap_report_id_survey_completions = None
        self.redcap_report_id_repeat_surveys = None
        self.redcap_report_id_participant_values = None
        self.redcap_report_id_participants = None

    __tablename__ = "study_redcap"

    redcap_api_token = db.Column(db.String, nullable=True)
    redcap_api_url = db.Column(db.String, nullable=True)
    redcap_project_id = db.Column(db.String, nullable=True)
    redcap_report_id_survey_completions = db.Column(db.String, nullable=True)
    redcap_report_id_repeat_surveys = db.Column(db.String, nullable=True)
    redcap_report_id_participant_values = db.Column(db.String, nullable=True)
    redcap_report_id_participants = db.Column(db.String, nullable=True)

    study_id = db.Column(
        db.CHAR(36),
        db.ForeignKey("study.id", ondelete="CASCADE"),
        primary_key=True,
        nullable=False,
    )
    study = db.relationship("Study", back_populates="study_redcap")

    def to_dict(self):
        """Converts the study to a dictionary"""
        return {
            "redcap_api_token": self.redcap_api_token,
            "redcap_api_url": self.redcap_api_url,
            "redcap_project_id": self.redcap_project_id,
            "redcap_report_id_survey_completions": self.redcap_report_id_survey_completions,
            "redcap_report_id_repeat_surveys": self.redcap_report_id_repeat_surveys,
            "redcap_report_id_participant_values": self.redcap_report_id_participant_values,
            "redcap_report_id_participants": self.redcap_report_id_participants
        }

    @staticmethod
    def from_data(study: Study, data: dict):
        """Creates a new study from a dictionary"""
        study_redcap = StudyRedcap(study)
        study_redcap.update(data)

        return study_redcap

    def update(self, data: dict):
        """Updates the study from a dictionary"""
        self.redcap_api_token = data["redcap_api_token"]
        self.redcap_api_url = data["redcap_api_url"]
        self.redcap_project_id = data["redcap_project_id"]
        self.redcap_report_id_survey_completions = data["redcap_report_id_survey_completions"]
        self.redcap_report_id_repeat_surveys = data["redcap_report_id_repeat_surveys"]
        self.redcap_report_id_participant_values = data["redcap_report_id_participant_values"]
        self.redcap_report_id_participants = data["redcap_report_id_participants"]
        self.study.touch()

    def validate(self):
        """Validates the study"""
        violations: list = []
        return violations
