import uuid

from ..db import db


class DatasetRights(db.Model):  # type: ignore
    def __init__(self, dataset):
        self.id = str(uuid.uuid4())
        self.dataset = dataset

    __tablename__ = "dataset_rights"
    id = db.Column(db.CHAR(36), primary_key=True)

    rights = db.Column(db.String, nullable=False)
    uri = db.Column(db.String, nullable=False)
    identifier = db.Column(db.String, nullable=False)
    identifier_scheme = db.Column(db.String, nullable=False)

    dataset_id = db.Column(db.CHAR(36), db.ForeignKey("dataset.id"), nullable=False)
    dataset = db.relationship("Dataset", back_populates="dataset_rights")

    def to_dict(self):
        return {
            "id": self.id,
            "rights": self.rights,
            "uri": self.uri,
            "identifier": self.identifier,
            "identifier_scheme": self.identifier_scheme,
        }

    @staticmethod
    def from_data(dataset, data: dict):
        dataset_rights = DatasetRights(dataset)
        dataset_rights.update(data)
        return dataset_rights

    def update(self, data: dict):
        self.rights = data["rights"]
        self.uri = data["uri"]
        self.identifier = data["identifier"]
        self.identifier_scheme = data["identifier_scheme"]
