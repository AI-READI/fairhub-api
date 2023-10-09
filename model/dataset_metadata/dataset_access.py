import uuid
from ..db import db


class DatasetAccess(db.Model):
    def __init__(self, dataset):
        self.id = str(uuid.uuid4())
        self.dataset = dataset

    __tablename__ = "dataset_access"
    id = db.Column(db.CHAR(36), primary_key=True)
    type = db.Column(db.String, nullable=False)
    description = db.Column(db.String, nullable=False)
    url = db.Column(db.String, nullable=False)
    url_last_checked = db.Column(db.String, nullable=False)

    dataset_id = db.Column(db.CHAR(36), db.ForeignKey("dataset.id"), nullable=False)
    dataset = db.relationship("Dataset", back_populates="dataset_access")

    def to_dict(self):
        return {
            "id": self.id,
            "type": self.type,
            "description": self.description,
            "url": self.url,
            "url_last_checked": self.url_last_checked,
        }

    @staticmethod
    def from_data(dataset, data: dict):
        dataset_access = DatasetAccess(dataset)
        dataset_access.update(data)
        return dataset_access

    def update(self, data):
        self.description = data["description"]
        self.url = data["url"]
        self.url_last_checked = data["url_last_checked"]
        self.type = data["type"]
