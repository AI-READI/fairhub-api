import uuid

from .db import db


class DatasetContributor(db.Model):
    def __init__(self):
        self.id = str(uuid.uuid4())

    __tablename__ = "dataset_contributor"
    id = db.Column(db.CHAR(36), primary_key=True)
    first_name = db.Column(db.String, nullable=False)
    last_name = db.Column(db.String, nullable=False)
    name_type = db.Column(db.String, nullable=False)
    name_identifier = db.Column(db.String, nullable=False)
    name_identifier_scheme = db.Column(db.String, nullable=False)
    name_identifier_scheme_uri = db.Column(db.String, nullable=False)
    creator = db.Column(db.BOOLEAN, nullable=False)
    contributor_type = db.Column(db.String, nullable=False)

    dataset_id = db.Column(db.CHAR(36), db.ForeignKey("dataset.id"))
    dataset = db.relationship("Dataset", back_populates="dataset_contributors")
    dataset_contributor_affiliation = db.relationship(
        "DatasetContributorAffiliation", back_populates="dataset_contributors")

    def to_dict(self):
        return {
            "id": self.id,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "name_type": self.name_type,
            "name_identifier": self.name_identifier,
            "name_identifier_scheme": self.name_identifier_scheme,
            "name_identifier_scheme_uri": self.name_identifier_scheme_uri,
            "creator": self.creator,
            "contributor_type": self.contributor_type,

        }


    @staticmethod
    def from_data(data: dict):
        dataset_contributor = DatasetContributor()
        dataset_contributor.first_name = data["first_name"]
        dataset_contributor.last_name = data["last_name"]
        dataset_contributor.name_type = data["name_type"]
        dataset_contributor.name_identifier = data["name_identifier"]
        dataset_contributor.name_identifier_scheme = data["name_identifier_scheme"]
        dataset_contributor.name_identifier_scheme_uri = data["name_identifier_scheme_uri"]
        dataset_contributor.creator = data["creator"]
        dataset_contributor.contributor_type = data["contributor_type"]
        return dataset_contributor
