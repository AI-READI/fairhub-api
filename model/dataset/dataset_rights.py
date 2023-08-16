import uuid
from ..db import db

class DatasetRights(db.Model):
    def __init__(self):
        self.id = str(uuid.uuid4())

    __tablename__ = "dataset_rights"
    id = db.Column(db.CHAR(36), primary_key=True)

    rights = db.Column(db.String, nullable=False)
    uri = db.Column(db.String, nullable=False)
    identifier = db.Column(db.String, nullable=False)
    identifier_scheme = db.Column(db.String, nullable=False)

    dataset_id = db.Column(db.CHAR(36), db.ForeignKey("dataset.id"))
    dataset = db.relationship(
        "Dataset", back_populates="dataset_rights"
    )

    def to_dict(self):
        return {
            "id": self.id,
            "rights": self.rights,
            "uri": self.uri,
            "identifier": self.identifier,
            "identifier_scheme": self.identifier_scheme,
        }

    @staticmethod
    def from_data(data: dict):
        dataset_rights = DatasetRights()
        dataset_rights.rights = data["rights"]
        dataset_rights.uri = data["uri"]
        dataset_rights.identifier = data["identifier"]
        dataset_rights.identifier_scheme = data["identifier_scheme"]
        return dataset_rights



