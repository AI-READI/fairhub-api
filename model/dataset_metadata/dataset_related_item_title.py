import uuid

from ..db import db


class DatasetRelatedItemTitle(db.Model):
    def __init__(self, dataset):
        self.id = str(uuid.uuid4())
        self.dataset = dataset

    __tablename__ = "dataset_related_item_title"
    id = db.Column(db.CHAR(36), primary_key=True)
    type = db.Column(db.String, nullable=False)
    title = db.Column(db.String, nullable=False)

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
        }

    @staticmethod
    def from_data(dataset, data: dict):
        dataset_related_item_title = DatasetRelatedItemTitle()
        dataset_related_item_title.update(data)
        return dataset_related_item_title

    def update(self, data: dict):
        self.type = data["type"]
        self.title = data["title"]
