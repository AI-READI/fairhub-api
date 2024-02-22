import uuid
import datetime
from datetime import timezone

from .db import db


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
