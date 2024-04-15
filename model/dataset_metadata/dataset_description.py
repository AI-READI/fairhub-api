import datetime
import uuid
from datetime import timezone

from ..db import db


class DatasetDescription(db.Model):  # type: ignore
    def __init__(self, dataset):
        self.id = str(uuid.uuid4())
        self.dataset = dataset
        self.created_at = datetime.datetime.now(timezone.utc).timestamp()
        self.description = ""
        self.type = "Abstract"

    __tablename__ = "dataset_description"
    id = db.Column(db.CHAR(36), primary_key=True)
    description = db.Column(db.String, nullable=False)
    type = db.Column(db.String, nullable=True)
    created_at = db.Column(db.BigInteger, nullable=False)

    dataset_id = db.Column(db.CHAR(36), db.ForeignKey("dataset.id"), nullable=False)
    dataset = db.relationship("Dataset", back_populates="dataset_description")

    def to_dict(self):
        return {
            "id": self.id,
            "description": self.description,
            "type": self.type,
            "created_at": self.created_at,
        }

    def to_dict_metadata(self):
        return {
            "id": self.id,
            "description": self.description,
            "type": self.type,
        }

    @staticmethod
    def from_data(dataset, data: dict):
        dataset_description = DatasetDescription(dataset)
        dataset_description.update(data)
        return dataset_description

    def update(self, data: dict):
        self.description = data["description"]
        self.type = data["type"]
        self.dataset.touch_dataset()
