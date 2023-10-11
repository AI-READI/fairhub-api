import uuid

from ..db import db


class DatasetRecordKeys(db.Model):
    def __init__(self, dataset):
        self.id = str(uuid.uuid4())
        self.dataset = dataset

    __tablename__ = "dataset_record_keys"
    id = db.Column(db.CHAR(36), primary_key=True)
    key_type = db.Column(db.String, nullable=False)
    key_details = db.Column(db.String, nullable=False)

    dataset_id = db.Column(db.CHAR(36), db.ForeignKey("dataset.id"), nullable=False)
    dataset = db.relationship("Dataset", back_populates="dataset_record_keys")

    def to_dict(self):
        return {
            "id": self.id,
            "key_type": self.key_type,
            "key_details": self.key_details,
        }

    @staticmethod
    def from_data(dataset, data: dict):
        dataset_record_keys = DatasetRecordKeys(dataset)
        dataset_record_keys.update(data)
        return dataset_record_keys

    def update(self, data):
        self.key_type = data["key_type"]
        self.key_details = data["key_details"]
