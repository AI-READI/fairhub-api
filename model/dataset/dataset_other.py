import uuid
from ..db import db


class DatasetRights(db.Model):
    def __init__(self):
        self.id = str(uuid.uuid4())

    __tablename__ = "dataset_other"
    id = db.Column(db.CHAR(36), primary_key=True)

    language = db.Column(db.String, nullable=False)
    managing_organization_name = db.Column(db.String, nullable=False)
    managing_organization_ror_id = db.Column(db.String, nullable=False)
    size = db.Column(db.String, nullable=False)

    dataset_id = db.Column(db.CHAR(36), db.ForeignKey("dataset.id"))
    dataset = db.relationship(
        "Dataset", back_populates="dataset_other"
    )

    def to_dict(self):
        return {
            "id": self.id,
            "language": self.language,
            "managing_organization_name": self.managing_organization_name,
            "managing_organization_ror_id": self.managing_organization_ror_id,
            "size": self.size,
        }

    @staticmethod
    def from_data(data: dict):
        dataset_other = DatasetRights()
        dataset_other.language = data["language"]
        dataset_other.managing_organization_name = data["managing_organization_name"]
        dataset_other.managing_organization_ror_id = data["managing_organization_ror_id"]
        dataset_other.size = data["size"]
        return dataset_other



