import uuid
import datetime
from datetime import timezone
from ..db import db


class DatasetRelatedItemTitle(db.Model):  # type: ignore
    def __init__(self, dataset):
        self.id = str(uuid.uuid4())
        self.dataset = dataset
        self.created_at = datetime.datetime.now(timezone.utc).timestamp()

    __tablename__ = "dataset_related_item_title"
    id = db.Column(db.CHAR(36), primary_key=True)
    type = db.Column(db.String, nullable=True)
    title = db.Column(db.String, nullable=False)
    created_at = db.Column(db.BigInteger, nullable=False)

    dataset_related_item_id = db.Column(
        db.CHAR(36), db.ForeignKey("related_item.id"), nullable=False
    )
    related_item = db.relationship(
        "DatasetRelatedItem", back_populates="related_item_title"
    )

    def to_dict(self):
        return {
            "id": self.id,
            "type": self.type,
            "title": self.title,
            "created_at": self.created_at

        }

    @staticmethod
    def from_data(dataset, data: dict):
        dataset_related_item_title = DatasetRelatedItemTitle(dataset)
        dataset_related_item_title.update(data)
        return dataset_related_item_title

    def update(self, data: dict):
        self.type = data["type"]
        self.title = data["title"]
