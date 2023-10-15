import uuid

from sqlalchemy import String
from sqlalchemy.dialects.postgresql import ARRAY

from ..db import db


class DatasetOther(db.Model):  # type: ignore
    def __init__(self, dataset):
        self.dataset = dataset

    __tablename__ = "dataset_other"

    resource_type = db.Column(db.String, nullable=False)
    language = db.Column(db.String, nullable=True)
    managing_organization_name = db.Column(db.String, nullable=False)
    managing_organization_ror_id = db.Column(db.String, nullable=False)
    size = db.Column(ARRAY(String), nullable=False)
    standards_followed = db.Column(db.String, nullable=False)
    acknowledgement = db.Column(db.String, nullable=False)
    publisher = db.Column(db.String, nullable=False)

    dataset_id = db.Column(db.CHAR(36), db.ForeignKey("dataset.id"), nullable=False)
    dataset = db.relationship("Dataset", back_populates="dataset_other")

    def to_dict(self):
        return {
            "language": self.language,
            "managing_organization_name": self.managing_organization_name,
            "managing_organization_ror_id": self.managing_organization_ror_id,
            "standards_followed": self.managing_organization_ror_id,
            "acknowledgement": self.acknowledgement,
            "size": self.size,
            "publisher": self.publisher,
            "resource_type": self.resource_type,
        }

    @staticmethod
    def from_data(dataset, data: dict):
        dataset_other = DatasetOther(dataset)
        dataset_other.update(data)
        return dataset_other

    def update(self, data: dict):
        self.language = data["language"]
        self.managing_organization_name = data["managing_organization_name"]
        self.managing_organization_ror_id = data["managing_organization_ror_id"]
        self.size = data["size"]
        self.acknowledgement = data["acknowledgement"]
        self.standards_followed = data["standards_followed"]
        self.publisher = data["publisher"]
        self.resource_type = data["resource_type"]

