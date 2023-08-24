import uuid
from ..db import db


class DatasetIdentifier(db.Model):
    def __init__(self, dataset):
        self.id = str(uuid.uuid4())
        self.dataset = dataset
    __tablename__ = "dataset_identifier"
    id = db.Column(db.CHAR(36), primary_key=True)
    identifier = db.Column(db.String, nullable=False)
    identifier_type = db.Column(db.String, nullable=False)
    alternate = db.Column(db.BOOLEAN, nullable=False)

    dataset_id = db.Column(db.CHAR(36), db.ForeignKey("dataset.id"))
    dataset = db.relationship("Dataset", back_populates="dataset_identifier")

    def to_dict(self):
        return {
            "id": self.id,
            "identifier": self.identifier,
            "identifier_type": self.identifier_type,
            "alternate": self.alternate,
        }

    @staticmethod
    def from_data(dataset, data: dict):
        dataset_date = DatasetIdentifier(dataset)
        dataset_date.update(data)
        return dataset_date

    def update(self, data):
        self.identifier = data["identifier"]
        self.identifier_type = data["identifier_type"]
        self.alternate = data["alternate"]

