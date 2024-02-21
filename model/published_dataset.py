import uuid
from .db import db
import datetime

from datetime import timezone


class PublishedDataset(db.Model):  # type: ignore
    """A published dataset is a collection of published datasets"""

    def __init__(self):
        self.id = str(uuid.uuid4())
        self.created_at = datetime.datetime.now(timezone.utc).timestamp()

    __tablename__ = "published_dataset"

    id = db.Column(db.CHAR(36), primary_key=True)
    study_id = db.Column(db.String, nullable=False)
    dataset_id = db.Column(db.String, nullable=False)
    version_id = db.Column(db.String, nullable=False)
    doi = db.Column(db.String, nullable=False)
    title = db.Column(db.String, nullable=False)
    description = db.Column(db.String, nullable=False)
    version_title = db.Column(db.String, nullable=False)
    study_title = db.Column(db.String, nullable=False)
    published_metadata = db.Column(db.JSON, nullable=False)
    files = db.Column(db.JSON, nullable=False)
    data = db.Column(db.JSON, nullable=False)
    created_at = db.Column(db.BigInteger, nullable=False)

    def to_dict(self):
        """Converts the published dataset to a dictionary"""
        return {
            "id": self.id,
            "study_id": self.study_id,
            "dataset_id": self.dataset_id,
            "version_id": self.version_id,
            "doi": self.doi,
            "title": self.title,
            "description": self.description,
            "version_title": self.version_title,
            "study_title": self.study_title,
            "published_metadata": self.published_metadata,
            "files": self.files,
            "data": self.data,
            "created_at": self.created_at,

        }

    @staticmethod
    def from_data(data: dict):
        """Creates a published dataset from a dictionary"""
        published_dataset = PublishedDataset()
        published_dataset.update(data)

        return published_dataset

    def update(self, data: dict):
        """Updates the published dataset from a dictionary"""
        # self.study_id = data["study_id"]
        # self.dataset_id = data["dataset_id"]
        # self.version_id = data["version_id"]
        # self.doi = data["doi"]
        # self.title = data["title"]
        self.description = data["description"]
        self.version_title = data["version_title"]
        self.study_title = data["study_title"]
        self.published_metadata = data["published_metadata"]
        self.files = data["files"]
        self.data = data["data"]

    def validate(self):
        """Validates the study"""
        violations: list = []
        return violations
