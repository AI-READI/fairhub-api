import uuid
from ..db import db


class DatasetAlternateIdentifier(db.Model):
    def __init__(self, dataset):
        self.id = str(uuid.uuid4())
        self.dataset = dataset

    __tablename__ = "dataset_alternate_identifier"
    id = db.Column(db.CHAR(36), primary_key=True)
    identifier = db.Column(db.String, nullable=False)
    identifier_type = db.Column(db.String, nullable=False)

    dataset_id = db.Column(db.CHAR(36), db.ForeignKey("dataset.id"), nullable=False)
    dataset = db.relationship("Dataset", back_populates="dataset_alternate_identifier")

    def to_dict(self):
        return {
            "id": self.id,
            "identifier": self.identifier,
            "identifier_type": self.identifier_type,
        }

    @staticmethod
    def from_data(dataset, data: dict):
        dataset_date = DatasetAlternateIdentifier(dataset)
        dataset_date.update(data)
        return dataset_date

    def update(self, data):
        self.identifier = data["identifier"]
        self.identifier_type = data["identifier_type"]
