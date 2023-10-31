import datetime
import uuid
from datetime import timezone

from ..db import db


class DatasetFunder(db.Model):  # type: ignore
    def __init__(self, dataset):
        self.id = str(uuid.uuid4())
        self.dataset = dataset
        self.created_at = datetime.datetime.now(timezone.utc).timestamp()

    __tablename__ = "dataset_funder"
    id = db.Column(db.CHAR(36), primary_key=True)
    name = db.Column(db.String, nullable=False)
    identifier = db.Column(db.String, nullable=False)
    identifier_type = db.Column(db.String, nullable=True)
    identifier_scheme_uri = db.Column(db.String, nullable=False)
    award_number = db.Column(db.String, nullable=False)
    award_uri = db.Column(db.String, nullable=False)
    award_title = db.Column(db.String, nullable=False)
    created_at = db.Column(db.BigInteger, nullable=False)

    dataset_id = db.Column(db.CHAR(36), db.ForeignKey("dataset.id"), nullable=False)
    dataset = db.relationship("Dataset", back_populates="dataset_funder")

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "identifier": self.identifier,
            "identifier_type": self.identifier_type,
            "identifier_scheme_uri": self.identifier_scheme_uri,
            "award_number": self.award_number,
            "award_uri": self.award_uri,
            "award_title": self.award_title,
            "created_at": self.created_at,
        }

    def to_dict_metadata(self):
        return {
            "id": self.id,
            "name": self.name,
        }

    @staticmethod
    def from_data(dataset, data: dict):
        dataset_funder = DatasetFunder(dataset)
        dataset_funder.update(data)
        return dataset_funder

    def update(self, data: dict):
        self.name = data["name"]
        self.identifier = data["identifier"]
        self.identifier_type = data["identifier_type"]
        self.identifier_scheme_uri = data["identifier_scheme_uri"]
        self.award_number = data["award_number"]
        self.award_uri = data["award_uri"]
        self.award_title = data["award_title"]
        self.dataset.touch_dataset()
