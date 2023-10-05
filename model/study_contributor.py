import uuid

from .db import db


class StudyContributor(db.Model):
    def __init__(self, study, user, permission):
        self.study = study
        self.user = user
        self.permission = permission

    __tablename__ = "study_contributor"
    permission = db.Column(db.String, nullable=False)
    user_id = db.Column(db.CHAR(36), db.ForeignKey("user.id"), primary_key=True)
    user = db.relationship(
        "User",
        back_populates="study_contributors",
    )

    study_id = db.Column(db.CHAR(36), db.ForeignKey("study.id"), primary_key=True)
    study = db.relationship("Study", back_populates="study_contributors")

    def to_dict(self):
        return {
            "user_id": self.user_id,
            "name": self.user.user_details.first_name
            if self.user.user_details
            else None,
            "email_address": self.user.email_address,
            "orcid": self.user.user_details.orcid if self.user.user_details else None,
            "role": self.permission,
            "status": "active",
        }

    @staticmethod
    def from_data(study, user, permission):
        contributor = StudyContributor(study, user, permission)
        return contributor

    def update(self, permission):
        self.permission = permission["permission"]
