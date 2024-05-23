import datetime
import uuid
from datetime import timezone

from ..db import db


class DatasetRelatedIdentifier(db.Model):  # type: ignore
    def __init__(self, dataset):
        self.id = str(uuid.uuid4())
        self.dataset = dataset
        self.created_at = datetime.datetime.now(timezone.utc).timestamp()

    __tablename__ = "dataset_related_identifier"

    id = db.Column(db.CHAR(36), primary_key=True)

    identifier = db.Column(db.String, nullable=False)
    identifier_type = db.Column(db.String, nullable=True)
    relation_type = db.Column(db.String, nullable=True)
    related_metadata_scheme = db.Column(db.String, nullable=False)
    scheme_uri = db.Column(db.String, nullable=False)
    scheme_type = db.Column(db.String, nullable=False)
    resource_type = db.Column(db.String, nullable=True)

    created_at = db.Column(db.BigInteger, nullable=False)

    dataset_id = db.Column(db.CHAR(36), db.ForeignKey("dataset.id"), nullable=False)
    dataset = db.relationship("Dataset", back_populates="dataset_related_identifier")

    def to_dict(self):
        return {
            "id": self.id,
            "identifier": self.identifier,
            "identifier_type": self.identifier_type,
            "relation_type": self.relation_type,
            "related_metadata_scheme": self.related_metadata_scheme,
            "scheme_uri": self.scheme_uri,
            "scheme_type": self.scheme_type,
            "resource_type": self.resource_type,
            "created_at": self.created_at,
        }

    def to_dict_metadata(self):
        return {
            "id": self.id,
            "identifier": self.identifier,
            "relation_type": self.relation_type,
            "resource_type": self.resource_type,
        }

    @staticmethod
    def from_data(dataset, data: dict):
        dataset_related_identifier = DatasetRelatedIdentifier(dataset)
        dataset_related_identifier.update(data)
        return dataset_related_identifier

    def update(self, data: dict):
        self.identifier = data["identifier"]
        self.identifier_type = data["identifier_type"]
        self.relation_type = data["relation_type"]
        self.related_metadata_scheme = data["related_metadata_scheme"]
        self.scheme_uri = data["scheme_uri"]
        self.scheme_type = data["scheme_type"]
        self.resource_type = data["resource_type"]

        self.dataset.touch_dataset()
