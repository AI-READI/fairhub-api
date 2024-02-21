import datetime
import uuid
from datetime import timezone

from model.db import db


class DatasetContributor(db.Model):  # type: ignore
    def __init__(self, dataset):
        self.id = str(uuid.uuid4())
        self.created_at = datetime.datetime.now(timezone.utc).timestamp()
        self.dataset = dataset

    __tablename__ = "dataset_contributor"
    id = db.Column(db.CHAR(36), primary_key=True)
    family_name = db.Column(db.String, nullable=True)
    given_name = db.Column(db.String, nullable=False)
    name_type = db.Column(db.String, nullable=True)
    name_identifier = db.Column(db.String, nullable=False)
    name_identifier_scheme = db.Column(db.String, nullable=False)
    name_identifier_scheme_uri = db.Column(db.String, nullable=False)
    creator = db.Column(db.BOOLEAN, nullable=False)
    contributor_type = db.Column(db.String, nullable=True)
    affiliations = db.Column(db.JSON, nullable=False)
    created_at = db.Column(db.BigInteger, nullable=False)

    dataset_id = db.Column(db.CHAR(36), db.ForeignKey("dataset.id"), nullable=False)
    dataset = db.relationship("Dataset", back_populates="dataset_contributors")

    def to_dict(self):
        return {
            "id": self.id,
            "given_name": self.given_name,
            "family_name": self.family_name,
            "name_type": self.name_type,
            "name_identifier": self.name_identifier,
            "name_identifier_scheme": self.name_identifier_scheme,
            "name_identifier_scheme_uri": self.name_identifier_scheme_uri,
            "creator": self.creator,
            "contributor_type": self.contributor_type,
            "affiliations": self.affiliations,
            "created_at": self.created_at,
        }

    def to_dict_metadata(self):
        return {
            "id": self.id,
            "given_name": self.given_name,
            "family_name": self.family_name,
            "name_type": self.name_type,
            "contributor_type": self.contributor_type,
            "creator": self.creator,
        }

    @staticmethod
    def from_data(dataset, data: dict):
        dataset_contributor = DatasetContributor(dataset)
        dataset_contributor.update(data)
        return dataset_contributor

    def update(self, data: dict):
        self.given_name = data["given_name"]
        self.family_name = data["family_name"]
        self.name_type = data["name_type"]
        self.name_identifier = data["name_identifier"]
        self.name_identifier_scheme = data["name_identifier_scheme"]
        self.name_identifier_scheme_uri = data["name_identifier_scheme_uri"]
        self.creator = data["creator"]
        self.contributor_type = data["contributor_type"]
        self.affiliations = data["affiliations"]
        self.dataset.touch_dataset()
