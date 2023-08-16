import uuid
from ..db import db


class DatasetContributorAffiliation(db.Model):
    def __init__(self):
        self.id = str(uuid.uuid4())

    __tablename__ = "dataset_contributor_affiliation"
    id = db.Column(db.CHAR(36), primary_key=True)
    description = db.Column(db.String, nullable=False)
    description_type = db.Column(db.String, nullable=False)

    dataset_id = db.Column(db.CHAR(36), db.ForeignKey("dataset.id"))
    dataset = db.relationship("Dataset", back_populates="dataset_contributors")

    def to_dict(self):
        return {
            "id": self.id,
            "description": self.description,
            "description_type": self.description_type,
        }

    @staticmethod
    def from_data(data: dict):
        dataset_contributor = DatasetContributorAffiliation()
        # dataset_contributor.id = data["id"]
        dataset_contributor.description = data["description"]
        dataset_contributor.description_type = data["description_type"]
        dataset_contributor.name_identifier_scheme_uri = data["identifier_scheme_uri"]
        return dataset_contributor
