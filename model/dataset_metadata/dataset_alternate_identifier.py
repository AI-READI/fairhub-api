import datetime
import uuid
from datetime import timezone

from ..db import db


class DatasetAlternateIdentifier(db.Model):  # type: ignore
    def __init__(self, dataset):
        self.id = str(uuid.uuid4())
        self.dataset = dataset
        self.created_at = datetime.datetime.now(timezone.utc).timestamp()

    __tablename__ = "dataset_alternate_identifier"
    id = db.Column(db.CHAR(36), primary_key=True)
    identifier = db.Column(db.String, nullable=False)
    type = db.Column(db.String, nullable=True)
    created_at = db.Column(db.BigInteger, nullable=False)

    dataset_id = db.Column(db.CHAR(36), db.ForeignKey("dataset.id"), nullable=False)
    dataset = db.relationship("Dataset", back_populates="dataset_alternate_identifier")

    def to_dict(self):
        return {
            "id": self.id,
            "identifier": self.identifier,
            "type": self.type,
            "created_at": self.created_at,
        }

    def to_dict_metadata(self):
        return {
            "id": self.id,
            "identifier": self.identifier,
        }

    @staticmethod
    def from_data(dataset, data: dict):
        dataset_date = DatasetAlternateIdentifier(dataset)
        dataset_date.update(data)
        return dataset_date

    def update(self, data: dict):
        self.identifier = data["identifier"]
        self.type = data["type"] if "type" in data else ""
        self.dataset.touch_dataset()
