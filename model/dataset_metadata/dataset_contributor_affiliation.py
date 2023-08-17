import uuid
from ..db import db


class DatasetContributorAffiliation(db.Model):
    def __init__(self):
        self.id = str(uuid.uuid4())

    __tablename__ = "dataset_contributor_affiliation"
    id = db.Column(db.CHAR(36), primary_key=True)
    identifier = db.Column(db.String, nullable=False)
    identifier_scheme = db.Column(db.String, nullable=False)
    identifier_scheme_uri = db.Column(db.String, nullable=False)
    dataset_contributors = db.relationship(
        "DatasetContributor", back_populates="dataset_contributor_affiliation"
    )
    dataset_contributor_id = db.Column(db.String, db.ForeignKey("dataset_contributor.id"))

    def to_dict(self):
        return {
            "id": self.id,
            "identifier": self.identifier,
            "identifier_scheme": self.identifier_scheme,
            "identifier_scheme_uri": self.identifier_scheme_uri,
        }

    @staticmethod
    def from_data(data: dict):
        dataset_contributor = DatasetContributorAffiliation()
        dataset_contributor.name_identifier = data["identifier"]
        dataset_contributor.name_identifier_scheme = data["identifier_scheme"]
        dataset_contributor.name_identifier_scheme_uri = data["identifier_scheme_uri"]
        return dataset_contributor
