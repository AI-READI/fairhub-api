import uuid

from .db import db


class StudyContributor(db.Model):
    def __init__(self):
        self.id = str(uuid.uuid4())

    __tablename__ = "study_contributor"
    permission = db.Column(db.String, nullable=False)
    user_id = db.Column(db.CHAR(36), db.ForeignKey("user.id"), primary_key=True)
    user = db.relationship("User", back_populates="study_contributors", )

    study_id = db.Column(db.CHAR(36), db.ForeignKey("study.id"), primary_key=True)
    study = db.relationship("Study", back_populates="study_contributors")

    def to_dict(self):
        return {
            "permission": self.permission,
            "user_id": self.user_id,
            "study_id": self.study_id,
        }

    @staticmethod
    def from_data(data: dict):
        study_contributor = StudyContributor()
        study_contributor.permission = data["permission"]
        study_contributor.user_id = data["user_id"]
        study_contributor.study_id = data["study_id"]
        return study_contributor
