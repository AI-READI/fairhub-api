from model import Study

from ..db import db


class StudyOther(db.Model):  # type: ignore
    """A study is a collection of datasets and participants"""

    def __init__(self, study):
        self.study = study
        self.size = 0

    __tablename__ = "study_other"

    size = db.Column(db.BigInteger, nullable=False)

    study_id = db.Column(
        db.CHAR(36),
        db.ForeignKey("study.id", ondelete="CASCADE"),
        primary_key=True,
        nullable=False,
    )
    study = db.relationship("Study", back_populates="study_other")

    def to_dict(self):
        """Converts the study to a dictionary"""
        return {
            "id": self.study_id,
            "size": self.size,
        }

    def to_dict_metadata(self):
        """Converts the study metadata to a dictionary"""
        return {
            "size": self.size,
        }

    @staticmethod
    def from_data(study: Study, data: dict):
        """Creates a new study from a dictionary"""
        study_other = StudyOther(study)
        study_other.update(data)

        return study_other

    def update(self, data: dict):
        """Updates the study from a dictionary"""

        self.size = data["size"]
        self.study.touch()

    def validate(self):
        """Validates the study"""
        violations: list = []
        return violations
