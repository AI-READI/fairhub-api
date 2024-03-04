from model import Study

from ..db import db


class StudyOversight(db.Model):  # type: ignore
    """A study is a collection of datasets and participants"""

    def __init__(self, study):
        self.study = study
        self.fda_regulated_drug = ""
        self.fda_regulated_device = ""
        self.human_subject_review_status = ""
        self.has_dmc = ""

    __tablename__ = "study_oversight"

    fda_regulated_drug = db.Column(db.String, nullable=False)
    fda_regulated_device = db.Column(db.String, nullable=False)
    human_subject_review_status = db.Column(db.String, nullable=False)
    has_dmc = db.Column(db.String, nullable=False)

    study_id = db.Column(
        db.CHAR(36),
        db.ForeignKey("study.id", ondelete="CASCADE"),
        primary_key=True,
        nullable=False,
    )
    study = db.relationship("Study", back_populates="study_oversight")

    def to_dict(self):
        """Converts the study to a dictionary"""
        return {
            "fda_regulated_drug": self.fda_regulated_drug,
            "fda_regulated_device": self.fda_regulated_device,
            "human_subject_review_status": self.human_subject_review_status,
            "has_dmc": self.has_dmc,
        }

    # def to_dict_metadata(self):
    #     """Converts the study metadata to a dictionary"""
    #     return {
    #         "fda_regulated_drug": self.oversight_has_dmc,
    #     }

    @staticmethod
    def from_data(study: Study, data: dict):
        """Creates a new study from a dictionary"""
        study_keywords = StudyOversight(study)
        study_keywords.update(data)

        return study_keywords

    def update(self, data: dict):
        """Updates the study from a dictionary"""
        self.fda_regulated_drug = data["fda_regulated_drug"]
        self.fda_regulated_device = data["fda_regulated_device"]
        self.human_subject_review_status = data["human_subject_review_status"]
        self.has_dmc = data["has_dmc"]
        self.study.touch()

    def validate(self):
        """Validates the study"""
        violations: list = []
        return violations
