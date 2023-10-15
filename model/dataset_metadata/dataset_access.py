from model import Dataset
import datetime

from ..db import db


class DatasetAccess(db.Model):  # type: ignore
    def __init__(self, dataset):
        self.dataset = dataset
        self.type = None
        self.description = ""
        self.url = ""
        self.url_last_checked = None

    __tablename__ = "dataset_access"
    type = db.Column(db.String, nullable=True)
    description = db.Column(db.String, nullable=False)
    url = db.Column(db.String, nullable=False)
    url_last_checked = db.Column(db.BigInteger, nullable=True)

    dataset_id = db.Column(db.CHAR(36), db.ForeignKey("dataset.id"), primary_key=True, nullable=False)
    dataset = db.relationship("Dataset", back_populates="dataset_access")

    def to_dict(self):
        return {
            "type": self.type,
            "description": self.description,
            "url": self.url,
        }

    @staticmethod
    def from_data(dataset: Dataset, data: dict):
        dataset_access = DatasetAccess(dataset)
        dataset_access.update(data)
        return dataset_access

    def update(self, data: dict):
        self.description = data["description"]
        self.url = data["url"]
        self.url_last_checked = datetime.datetime.now(datetime.timezone.utc).timestamp()
        self.type = data["type"]
