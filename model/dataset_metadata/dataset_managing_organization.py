import uuid

from ..db import db


class DatasetManagingOrganization(db.Model):
    def __init__(self, dataset):
        self.id = str(uuid.uuid4())
        self.dataset = dataset

    __tablename__ = "dataset_managing_organization"
    id = db.Column(db.CHAR(36), primary_key=True)

    name = db.Column(db.String, nullable=False)
    ror_id = db.Column(db.String, nullable=False)

    dataset_id = db.Column(db.CHAR(36), db.ForeignKey("dataset.id"), nullable=False)
    dataset = db.relationship("Dataset", back_populates="dataset_managing_organization")

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "ror_id": self.ror_id,
        }

    @staticmethod
    def from_data(dataset, data: dict):
        dataset_managing_organization = DatasetManagingOrganization(dataset)
        dataset_managing_organization.update(data)
        return dataset_managing_organization

    def update(self, data: dict):
        self.name = data["name"]
        self.ror_id = data["ror_id"]
