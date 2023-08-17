import uuid
from ..db import db


class DatasetDescription(db.Model):
    def __init__(self):
        self.id = str(uuid.uuid4())

    __tablename__ = "dataset_description"
    id = db.Column(db.CHAR(36), primary_key=True)
    description = db.Column(db.String, nullable=False)
    description_type = db.Column(db.String, nullable=False)

    dataset_id = db.Column(db.CHAR(36), db.ForeignKey("dataset.id"))
    dataset = db.relationship(
        "Dataset", back_populates="dataset_description"
    )

    def to_dict(self):
        return {
            "id": self.id,
            "description": self.description,
            "description_type": self.description_type,
        }

    @staticmethod
    def from_data(data: dict):
        dataset_description = DatasetDescription()
        dataset_description.description = data["description"]
        dataset_description.description_type = data["description_type"]
        dataset_description.name_identifier_scheme_uri = data["identifier_scheme_uri"]
        return dataset_description
