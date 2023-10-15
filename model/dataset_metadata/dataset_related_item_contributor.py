import uuid
import datetime
from datetime import timezone
from ..db import db


class DatasetRelatedItemContributor(db.Model):  # type: ignore
    def __init__(self, dataset):
        self.id = str(uuid.uuid4())
        self.dataset = dataset
        self.created_at = datetime.datetime.now(timezone.utc).timestamp()

    __tablename__ = "dataset_related_item_contributor"
    id = db.Column(db.CHAR(36), primary_key=True)
    name = db.Column(db.String, nullable=False)
    name_type = db.Column(db.String, nullable=True)
    creator = db.Column(db.BOOLEAN, nullable=False)
    contributor_type = db.Column(db.String, nullable=True)
    created_at = db.Column(db.BigInteger, nullable=False)

    dataset_related_item_id = db.Column(
        db.CHAR(36), db.ForeignKey("dataset_related_item.id"), nullable=False
    )
    dataset_related_item = db.relationship(
        "DatasetRelatedItem", back_populates="dataset_related_item_contributor"
    )

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "name_type": self.name_type,
            "creator": self.creator,
            "contributor_type": self.contributor_type,
            "created_at": self.created_at

        }

    @staticmethod
    def from_data(dataset, data: dict):
        dataset_related_contributor = DatasetRelatedItemContributor(dataset)
        dataset_related_contributor.update(data)
        return dataset_related_contributor

    def update(self, data: dict):
        self.name = data["name"]
        self.name_type = data["name_type"]
        self.creator = data["creator"]
        self.contributor_type = data["contributor_type"]
