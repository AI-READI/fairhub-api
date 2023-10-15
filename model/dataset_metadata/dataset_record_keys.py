from ..db import db


class DatasetRecordKeys(db.Model):  # type: ignore
    def __init__(self, dataset):
        self.dataset = dataset
        self.key_type = None
        self.key_details = ""
    __tablename__ = "dataset_record_keys"
    key_type = db.Column(db.String, nullable=True)
    key_details = db.Column(db.String, nullable=False)

    dataset_id = db.Column(db.CHAR(36), db.ForeignKey("dataset.id"), primary_key=True, nullable=False)
    dataset = db.relationship("Dataset", back_populates="dataset_record_keys")

    def to_dict(self):
        return {
            "key_type": self.key_type,
            "key_details": self.key_details,
        }

    @staticmethod
    def from_data(dataset, data: dict):
        dataset_record_keys = DatasetRecordKeys(dataset)
        dataset_record_keys.update(data)
        return dataset_record_keys

    def update(self, data: dict):
        self.key_type = data["key_type"]
        self.key_details = data["key_details"]
