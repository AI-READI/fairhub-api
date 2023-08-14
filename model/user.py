import uuid
from datetime import  datetime
from .db import db


class User(db.Model):
    def __init__(self):
        self.id = str(uuid.uuid4())

    __tablename__ = "user"
    id = db.Column(db.CHAR(36), primary_key=True)
    email_address = db.Column(db.String, nullable=False)
    username = db.Column(db.String, nullable=False)
    first_name = db.Column(db.String, nullable=False)
    last_name = db.Column(db.String, nullable=False)
    orcid = db.Column(db.String, nullable=False)
    hash = db.Column(db.String, nullable=False)
    created_at = db.Column(db.DateTime, nullable=False)
    institution = db.Column(db.String, nullable=False)
    study_contributors = db.relationship("StudyContributor", back_populates="user")
    def to_dict(self):
        return {
            "id": self.id,
            "email_address": self.email_address,
            "username": self.username,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "orcid": self.orcid,
            "hash": self.hash,
            "created_at": str(datetime.now()),
            "institution": self.institution,
        }

    @staticmethod
    def from_data(data: dict):
        user = User()
        user.email_address = data["email_address"]
        user.username = data["username"]
        user.first_name = data["first_name"]
        user.last_name = data["last_name"]
        user.orcid = data["orcid"]
        user.hash = data["hash"]
        user.created_at = data["created_at"]
        user.institution = data["institution"]
        return user
