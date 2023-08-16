import uuid
from ..db import db


class DatasetManagingOrganization(db.Model):
    def __init__(self):
        self.id = str(uuid.uuid4())

    __tablename__ = "dataset_managing_organization"
    id = db.Column(db.CHAR(36), primary_key=True)

    name = db.Column(db.String, nullable=False)
    ror_id = db.Column(db.String, nullable=False)

    dataset_id = db.Column(db.CHAR(36), db.ForeignKey("dataset.id"))
    dataset = db.relationship(
        "Dataset", back_populates="dataset_managing_organization"
    )

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "ror_id": self.ror_id,
        }

    @staticmethod
    def from_data(data: dict):
        dataset_managing_organization = DatasetManagingOrganization()
        dataset_managing_organization.name = data["name"]
        dataset_managing_organization.ror_id = data["ror_id"]
        return dataset_managing_organization



