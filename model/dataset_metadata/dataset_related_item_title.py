import datetime
import uuid
from datetime import timezone

from ..db import db


class DatasetRelatedItemTitle(db.Model):  # type: ignore
    def __init__(self, dataset_related_item):
        self.id = str(uuid.uuid4())
        self.dataset_related_item = dataset_related_item
        self.created_at = datetime.datetime.now(timezone.utc).timestamp()

    __tablename__ = "dataset_related_item_title"
    id = db.Column(db.CHAR(36), primary_key=True)
    type = db.Column(db.String, nullable=True)
    title = db.Column(db.String, nullable=False)
    created_at = db.Column(db.BigInteger, nullable=False)

    dataset_related_item_id = db.Column(
        db.CHAR(36), db.ForeignKey("dataset_related_item.id"), nullable=False
    )
    dataset_related_item = db.relationship(
        "DatasetRelatedItem", back_populates="dataset_related_item_title"
    )

    def to_dict(self):
        return {
            "id": self.id,
            "type": self.type,
            "title": self.title,
            "created_at": self.created_at,
        }

    def to_dict_metadata(self):
        return {
            "id": self.id,
            "title": self.title,
            "type": self.type,
        }

    @staticmethod
    def from_data(dataset_related_item, data: dict):
        dataset_related_item_title = DatasetRelatedItemTitle(dataset_related_item)
        dataset_related_item_title.update(data)
        return dataset_related_item_title

    def update(self, data: dict):
        self.type = data["type"]
        self.title = data["title"]
