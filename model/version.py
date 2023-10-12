import datetime
import uuid
from datetime import timezone

from model.dataset import Dataset

from .db import db

version_participants = db.Table(
    "version_participants",
    db.Model.metadata,
    db.Column("dataset_version_id", db.ForeignKey("version.id"), primary_key=True),
    db.Column("participant_id", db.ForeignKey("participant.id"), primary_key=True),
)


class Version(db.Model):
    def __init__(self, dataset):
        self.dataset = dataset
        self.id = str(uuid.uuid4())

    __tablename__ = "version"
    id = db.Column(db.CHAR(36), primary_key=True)

    title = db.Column(db.String, nullable=False)
    published = db.Column(db.BOOLEAN, nullable=False)
    changelog = db.Column(db.String, nullable=False)
    updated_on = db.Column(db.BigInteger, nullable=False)
    doi = db.Column(db.String, nullable=False)
    created_at = db.Column(db.BigInteger, nullable=False)
    published_on = db.Column(db.BigInteger, nullable=False)

    dataset_id = db.Column(db.CHAR(36), db.ForeignKey("dataset.id"), nullable=False)
    dataset = db.relationship("Dataset", back_populates="dataset_versions")
    participants = db.relationship("Participant", secondary=version_participants)

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "changelog": self.changelog,
            "published_on": self.published_on,
            "updated_on": self.updated_on,
            "created_at": self.created_at,
            "doi": self.doi,
            "published": self.published,
            "participants": [p.id for p in self.participants],
        }

    @staticmethod
    def from_data(dataset: Dataset, data: dict):
        dataset_version_obj = Version(dataset)
        dataset_version_obj.update(data)
        return dataset_version_obj

    def update(self, data: dict):
        self.title = data["title"]
        self.published = data["published"]
        self.doi = data["doi"]
        self.published_on = datetime.datetime.now(timezone.utc).timestamp()
        self.updated_on = datetime.datetime.now(timezone.utc).timestamp()
        self.participants[:] = data["participants"]
        self.changelog = data["changelog"]
