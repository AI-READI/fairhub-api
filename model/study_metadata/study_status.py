import uuid

from ..db import db


class StudyStatus(db.Model):
    """A study is a collection of datasets and participants"""

    def __init__(self, study):
        self.id = str(uuid.uuid4())
        self.study = study
        self.overall_status = None
        self.why_stopped = ""
        self.start_date = None
        self.start_date_type = None
        self.completion_date = None
        self.completion_date_type = None

    __tablename__ = "study_status"

    id = db.Column(db.CHAR(36), primary_key=True)
    overall_status = db.Column(db.String, nullable=True)
    why_stopped = db.Column(db.String, nullable=False)
    start_date = db.Column(db.String, nullable=True)
    start_date_type = db.Column(db.String, nullable=True)
    completion_date = db.Column(db.String, nullable=True)
    completion_date_type = db.Column(db.String, nullable=True)

    study_id = db.Column(db.CHAR(36), db.ForeignKey("study.id"))
    study = db.relationship("Study", back_populates="study_status")

    def to_dict(self):
        """Converts the study to a dictionary"""
        return {
            "id": self.id,
            "overall_status": self.overall_status,
            "why_stopped": self.why_stopped,
            "start_date": self.start_date,
            "start_date_type": self.start_date_type,
            "completion_date": self.completion_date,
            "completion_date_type": self.completion_date_type,
        }

    @staticmethod
    def from_data(study, data: dict):
        """Creates a new study from a dictionary"""
        study_status = StudyStatus(study)
        study_status.update(data)

        return study_status

    def update(self, data):
        """Updates the study from a dictionary"""
        self.overall_status = data["overall_status"]
        self.why_stopped = data["why_stopped"]
        self.start_date = data["start_date"]
        self.start_date_type = data["start_date_type"]
        self.completion_date = data["completion_date"]
        self.completion_date_type = data["completion_date_type"]
        self.study.touch()

    def validate(self):
        """Validates the study"""
        violations = []
        return violations
