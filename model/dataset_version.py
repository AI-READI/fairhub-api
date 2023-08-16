import uuid
from datetime import datetime
from model import Dataset

from .db import db

version_participants = db.Table(
    "version_participants",
    db.Model.metadata,
    db.Column(
        "dataset_version_id", db.ForeignKey("dataset_version.id"), primary_key=True
    ),
    db.Column("participant_id", db.ForeignKey("participant.id"), primary_key=True),
)


class DatasetVersion(db.Model):
    def __init__(self, dataset):
        self.dataset = dataset
        self.id = str(uuid.uuid4())

    __tablename__ = "dataset_version"
    id = db.Column(db.CHAR(36), primary_key=True)

    title = db.Column(db.String, nullable=False)
    published = db.Column(db.BOOLEAN, nullable=False)
    changelog = db.Column(db.String, nullable=False)
    updated_on = db.Column(db.DateTime, nullable=False)
    doi = db.Column(db.String, nullable=False)
    created_at = db.Column(db.DateTime, nullable=False)
    published_on = db.Column(db.DateTime, nullable=False)

    dataset_id = db.Column(db.CHAR(36), db.ForeignKey("dataset.id"))
    dataset = db.relationship("Dataset", back_populates="dataset_versions")
    participants = db.relationship("Participant", secondary=version_participants)

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "changelog": self.changelog,
            "published_on": str(datetime.now()),
            "created_at": str(datetime.now()),
            "doi": self.doi,
            "published": self.published,
            "participants": [p.id for p in self.participants],
        }

    @staticmethod
    def from_data(dataset: Dataset, data: dict):
        dataset_version_obj = DatasetVersion(dataset)
        dataset_version_obj.update(data)
        return dataset_version_obj

    def update(self, data):
        self.title = data["title"]
        self.published = data["published"]
        self.doi = data["doi"]
        self.created_at = data["created_at"]
        self.published_on = data["published_on"]
        self.participants[:] = data["participants"]
        self.changelog = data["changelog"]


