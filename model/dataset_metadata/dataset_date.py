import datetime
import uuid
from datetime import timezone

from ..db import db


class DatasetDate(db.Model):  # type: ignore
    def __init__(self, dataset):
        self.id = str(uuid.uuid4())
        self.dataset = dataset
        self.created_at = datetime.datetime.now(timezone.utc).timestamp()

    __tablename__ = "dataset_date"
    id = db.Column(db.CHAR(36), primary_key=True)

    date = db.Column(db.BigInteger, nullable=True)
    type = db.Column(db.String, nullable=True)
    information = db.Column(db.String, nullable=False)
    created_at = db.Column(db.BigInteger, nullable=False)

    dataset_id = db.Column(db.CHAR(36), db.ForeignKey("dataset.id"), nullable=False)
    dataset = db.relationship("Dataset", back_populates="dataset_date")

    def to_dict(self):
        return {
            "id": self.id,
            "date": self.date,
            "type": self.type,
            "information": self.information,
            "created_at": self.created_at,
        }

    def to_dict_metadata(self):
        return {
            "id": self.id,
            "date": self.date,
        }

    @staticmethod
    def from_data(dataset, data: dict):
        dataset_date = DatasetDate(dataset)
        dataset_date.update(data)
        return dataset_date

    def update(self, data: dict):
        self.date = data["date"]
        self.type = data["type"]
        self.information = data["information"]
        self.dataset.touch_dataset()
