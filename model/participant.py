import datetime
import uuid
from datetime import timezone

import model
from .study import Study
from .db import db


class Participant(db.Model):  # type: ignore
    def __init__(self, study):
        self.study = study
        self.id = str(uuid.uuid4())
        self.created_at = datetime.datetime.now(timezone.utc).timestamp()

    __tablename__ = "participant"
    id = db.Column(db.CHAR(36), primary_key=True)
    first_name = db.Column(db.String, nullable=False)
    last_name = db.Column(db.String, nullable=False)
    address = db.Column(db.String, nullable=False)
    age = db.Column(db.String, nullable=False)
    created_at = db.Column(db.BigInteger, nullable=False)
    updated_on = db.Column(db.BigInteger, nullable=False)

    study_id = db.Column(
        db.CHAR(36), db.ForeignKey("study.id", ondelete="CASCADE"), nullable=False
    )
    study = db.relationship("Study", back_populates="participants")
    dataset_versions = db.relationship(
        "Version",
        back_populates="participants",
        secondary=model.version.version_participants,
    )

    def to_dict(self):
        return {
            "id": self.id,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "address": self.address,
            "age": self.age,
            "created_at": self.created_at,
            "updated_on": self.updated_on,
        }

    @staticmethod
    def from_data(data: dict, study: Study):
        participant = Participant(study)
        participant.update(data)
        return participant

    def update(self, data: dict):
        self.first_name = data["first_name"]
        self.last_name = data["last_name"]
        self.address = data["address"]
        self.age = data["age"]
        self.updated_on = datetime.datetime.now(timezone.utc).timestamp()
