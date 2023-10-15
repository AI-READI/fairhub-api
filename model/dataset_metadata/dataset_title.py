import uuid
import datetime
from datetime import timezone

from ..db import db


class DatasetTitle(db.Model):  # type: ignore
    def __init__(self, dataset):
        self.id = str(uuid.uuid4())
        self.dataset = dataset
        self.created_at = datetime.datetime.now(timezone.utc).timestamp()

    __tablename__ = "dataset_title"
    id = db.Column(db.CHAR(36), primary_key=True)
    title = db.Column(db.String, nullable=False)
    type = db.Column(db.String, nullable=True)
    created_at = db.Column(db.BigInteger, nullable=False)

    dataset = db.relationship("Dataset", back_populates="dataset_title")
    dataset_id = db.Column(db.String, db.ForeignKey("dataset.id"), nullable=False)

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "type": self.type,
            "created_at": self.created_at,

        }

    @staticmethod
    def from_data(dataset, data: dict):
        dataset_title = DatasetTitle(dataset)
        dataset_title.update(data)

        return dataset_title

    def update(self, data: dict):
        self.title = data["title"]
        self.type = data["type"]
