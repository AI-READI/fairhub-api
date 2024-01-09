import datetime
import uuid
from datetime import timezone
from sqlalchemy import Table, Sequence

import model
from model.dataset import Dataset

from .db import db

version_participants: Table = db.Table(
    "version_participants",
    db.Model.metadata,
    db.Column("dataset_version_id", db.ForeignKey("version.id"), primary_key=True),
    db.Column("participant_id", db.ForeignKey("participant.id"), primary_key=True),
)


class Version(db.Model):  # type: ignore
    def __init__(self, dataset):
        self.dataset = dataset
        self.id = str(uuid.uuid4())
        self.created_at = datetime.datetime.now(timezone.utc).timestamp()
        self.version_readme = model.VersionReadme(self)

    __tablename__ = "version"
    id = db.Column(db.CHAR(36), primary_key=True)

    title = db.Column(db.String, nullable=False)
    published = db.Column(db.BOOLEAN, nullable=False)
    changelog = db.Column(db.String, nullable=False)
    updated_on = db.Column(db.BigInteger, nullable=False)
    created_at = db.Column(db.BigInteger, nullable=False)
    published_on = db.Column(db.BigInteger, nullable=False)

    identifier = db.Column(db.Integer,
                           Sequence('identifier_seq'),
                           nullable=False,
                           unique=True,
                           server_default=Sequence('identifier_seq').next_value())

    doi = db.Column(db.String, nullable=True)

    version_readme = db.relationship(
        "VersionReadme",
        uselist=False,
        back_populates="version",
        cascade="all, delete",
    )
    dataset_id = db.Column(db.CHAR(36), db.ForeignKey("dataset.id"), nullable=False)
    dataset = db.relationship("Dataset", back_populates="dataset_versions")
    participants = db.relationship(
        "Participant",
        secondary=version_participants,
        cascade="all, delete",
    )

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "changelog": self.changelog,
            "published_on": self.published_on,
            "updated_on": self.updated_on,
            "created_at": self.created_at,
            "identifier": self.identifier,
            "doi": self.doi,
            "published": self.published,
            "readme": self.version_readme.content if self.version_readme else ""
            # "participants": [p.id for p in self.participants]
            # if isinstance(self.participants, (list, set))
            # else [],
        }

    # [p.id for p in self.participants]

    @staticmethod
    def from_data(dataset: Dataset, data: dict):
        dataset_version_obj = Version(dataset)
        dataset_version_obj.update(data)
        return dataset_version_obj

    def update(self, data: dict):
        self.title = data["title"]
        self.published = data["published"] if "published" in data else False
        self.published_on = datetime.datetime.now(timezone.utc).timestamp()
        self.updated_on = datetime.datetime.now(timezone.utc).timestamp()
        # self.participants[:] = data["participants"]
        self.changelog = data["changelog"] if "changelog" in data else ""
