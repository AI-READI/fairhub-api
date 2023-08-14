import uuid

import model
from datetime import datetime
from .db import db


class Participant(db.Model):
    def __init__(self, study):
        self.study = study
        self.id = str(uuid.uuid4())

    __tablename__ = "participant"
    id = db.Column(db.CHAR(36), primary_key=True)
    first_name = db.Column(db.String, nullable=False)
    last_name = db.Column(db.String, nullable=False)
    address = db.Column(db.String, nullable=False)
    age = db.Column(db.String, nullable=False)
    created_at = db.Column(db.DateTime, nullable=False)
    updated_on = db.Column(db.DateTime, nullable=False)

    study_id = db.Column(db.CHAR(36), db.ForeignKey("study.id"))
    study = db.relationship("Study", back_populates="participants")
    dataset_versions = db.relationship(
        "DatasetVersion",
        back_populates="participants",
        secondary=model.dataset_version.version_participants,
    )

    def to_dict(self):
        return {
            "id": self.id,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "address": self.address,
            "age": self.age,
            "created_at" : str(datetime.now()),
            "published_on": str(datetime.now()),
        }

    @staticmethod
    def from_data(data: dict, study):
        participant = Participant(study)
        participant.update(data)
        return participant

    def update(self, data):
        # self.id = data["id"]
        self.first_name = data["first_name"]
        self.last_name = data["last_name"]
        self.address = data["address"]
        self.age = data["age"]
        self.created_at = data["created_at"]
        self.updated_on = data["updated_on"]
