from model import Study

from ..db import db


class StudyDescription(db.Model):  # type: ignore
    """A study is a collection of datasets and participants"""

    def __init__(self, study: Study):
        self.study = study
        self.brief_summary = ""
        self.detailed_description = ""

    __tablename__ = "study_description"

    brief_summary = db.Column(db.String, nullable=False)
    detailed_description = db.Column(db.String, nullable=False)

    study_id = db.Column(
        db.CHAR(36),
        db.ForeignKey("study.id", ondelete="CASCADE"),
        primary_key=True,
        nullable=False,
    )
    study = db.relationship("Study", back_populates="study_description")

    def to_dict(self):
        """Converts the study to a dictionary"""
        return {
            "brief_summary": self.brief_summary,
            "detailed_description": self.detailed_description,
        }

    def to_dict_metadata(self):
        """Converts the study metadata to a dictionary"""
        return {
            "brief_summary": self.brief_summary
        }

    @staticmethod
    def from_data(study: Study, data: dict):
        """Creates a new study from a dictionary"""
        study_description = StudyDescription(study)
        study_description.update(data)

        return study_description

    def update(self, data: dict):
        """Updates the study from a dictionary"""
        self.brief_summary = data["brief_summary"]
        self.detailed_description = data["detailed_description"]
        self.study.touch()

    def validate(self):
        """Validates the lead_sponsor_last_name study"""
        violations: list = []
        return violations
