import datetime

from .db import db
from .study import Study
from .user import User

# from datetime import datetime, timezone


class StudyContributor(db.Model):  # type: ignore
    def __init__(self, study: Study, user: User, permission):
        self.study = study
        self.user = user
        self.permission = permission
        self.created_at = datetime.datetime.now(datetime.timezone.utc).timestamp()

    __tablename__ = "study_contributor"
    permission = db.Column(db.String, nullable=False)
    user_id = db.Column(db.CHAR(36), db.ForeignKey("user.id"), primary_key=True)
    created_at = db.Column(db.BigInteger, nullable=False)

    user = db.relationship(
        "User",
        back_populates="study_contributors",
    )

    study_id = db.Column(db.CHAR(36), db.ForeignKey("study.id"), primary_key=True)
    study = db.relationship("Study", back_populates="study_contributors")

    def to_dict(self):
        return {
            "id": self.user_id,
            "name": (
                self.user.user_details.first_name if self.user.user_details else None
            ),
            "email_address": self.user.email_address,
            "orcid": self.user.user_details.orcid if self.user.user_details else None,
            "role": self.permission,
            "status": "accepted",
        }

    @staticmethod
    def from_data(study: Study, user: User, permission):
        contributor = StudyContributor(study, user, permission)
        return contributor

    def update(self, permission):
        self.permission = permission["permission"]
