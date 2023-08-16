import uuid
from ..db import db


class DatasetFunder(db.Model):
    def __init__(self):
        self.id = str(uuid.uuid4())

    __tablename__ = "dataset_funder"
    id = db.Column(db.CHAR(36), primary_key=True)
    name = db.Column(db.String, nullable=False)
    identifier = db.Column(db.String, nullable=False)
    identifier_type = db.Column(db.String, nullable=False)
    identifier_scheme_uri = db.Column(db.String, nullable=False)
    award_number = db.Column(db.String, nullable=False)
    award_uri = db.Column(db.String, nullable=False)
    award_title = db.Column(db.String, nullable=False)

    dataset_id = db.Column(db.CHAR(36), db.ForeignKey("dataset.id"))
    dataset = db.relationship(
        "Dataset", back_populates="dataset_funder"
    )

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
        }

    @staticmethod
    def from_data(data: dict):
        dataset_funder = DatasetFunder()
        dataset_funder.name = data["name"]
        dataset_funder.identifier = data["identifier"]
        dataset_funder.identifier_type = data["identifier_type"]
        dataset_funder.identifier_scheme_uri = data["identifier_scheme_uri"]
        dataset_funder.award_number = data["award_number"]
        dataset_funder.award_uri = data["award_uri"]
        dataset_funder.award_title = data["award_title"]

        return dataset_funder
