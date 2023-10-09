import uuid
from ..db import db


class DatasetDescription(db.Model):
    def __init__(self, dataset):
        self.id = str(uuid.uuid4())
        self.dataset = dataset

    __tablename__ = "dataset_description"
    id = db.Column(db.CHAR(36), primary_key=True)
    description = db.Column(db.String, nullable=False)
    description_type = db.Column(db.String, nullable=False)

    dataset_id = db.Column(db.CHAR(36), db.ForeignKey("dataset.id"), nullable=False)
    dataset = db.relationship("Dataset", back_populates="dataset_description")

    def to_dict(self):
        return {
            "id": self.id,
            "description": self.description,
            "description_type": self.description_type,
        }

    @staticmethod
    def from_data(dataset, data: dict):
        dataset_description = DatasetDescription(dataset)
        dataset_description.update(data)
        return dataset_description

    def update(self, data):
        self.description = data["description"]
        self.description_type = data["description_type"]
