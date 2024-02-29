import datetime
import uuid
from datetime import timezone

from ..db import db


class DatasetPublisher(db.Model):  # type: ignore
    def __init__(self, dataset):
        self.id = str(uuid.uuid4())
        self.dataset = dataset
        self.publisher = ""
        self.identifier = ""
        self.identifier_scheme = ""
        self.scheme_uri = ""
    __tablename__ = "dataset_publisher"

    publisher = db.Column(db.String, nullable=False)
    identifier = db.Column(db.String, nullable=False)
    identifier_scheme = db.Column(db.String, nullable=False)
    scheme_uri = db.Column(db.String, nullable=False)

    dataset_id = db.Column(db.CHAR(36), db.ForeignKey("dataset.id"), primary_key=True, nullable=False)
    dataset = db.relationship("Dataset", back_populates="dataset_publisher")

    def to_dict(self):
        return {
            "publisher": self.publisher,
            "identifier": self.identifier,
            "identifier_scheme": self.identifier_scheme,
            "scheme_uri": self.scheme_uri,

        }

    # def to_dict_metadata(self):
    #     return {
    #         "id": self.id,
    #         "subject": self.subject,
    #         "scheme": self.scheme,
    #     }

    @staticmethod
    def from_data(dataset, data: dict):
        dataset_subject = DatasetPublisher(dataset)
        dataset_subject.update(data)
        return dataset_subject

    def update(self, data: dict):
        self.publisher = data["publisher_name"]
        self.identifier = data["publisher_identifier"]
        self.identifier_scheme = data["publisher_identifier_scheme"]
        self.scheme_uri = data["publisher_identifier_scheme_uri"]
        self.dataset.touch_dataset()
