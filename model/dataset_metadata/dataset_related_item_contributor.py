import datetime
import uuid
from datetime import timezone

from ..db import db


class DatasetRelatedItemContributor(db.Model):  # type: ignore
    def __init__(self, dataset_related_item, creator):
        self.id = str(uuid.uuid4())
        self.dataset_related_item = dataset_related_item
        self.created_at = datetime.datetime.now(timezone.utc).timestamp()
        self.creator = creator

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
            "contributor_type": self.contributor_type,
            "created_at": self.created_at,
        }

    @staticmethod
    def from_data(dataset_related_item, data: dict, creator):
        contributor_ = DatasetRelatedItemContributor(dataset_related_item, creator)
        contributor_.update(data)
        return contributor_

    def update(self, data: dict):
        self.name = data["name"] \
            if "name" in data else ""
        self.name_type = data["name_type"] \
            if "name_type" in data else None
        self.contributor_type = (
            data["contributor_type"]
            if "contributor_type" in data else None
        )
