import uuid
from ..db import db


class DatasetRelatedItem(db.Model):
    def __init__(self):
        self.id = str(uuid.uuid4())

    __tablename__ = "dataset_related_item"
    id = db.Column(db.CHAR(36), primary_key=True)
    type = db.Column(db.String, nullable=False)
    relation_type = db.Column(db.String, nullable=False)

    dataset_id = db.Column(db.CHAR(36), db.ForeignKey("dataset.id"))
    dataset = db.relationship("Dataset", back_populates="dataset_related_item")

    def to_dict(self):
        return {
            "id": self.id,
            "type": self.type,
            "relation_type": self.relation_type,
        }

    @staticmethod
    def from_data(data: dict):
        dataset_related_item = DatasetRelatedItem()
        dataset_related_item.type = data["type"]
        dataset_related_item.relation_type = data["relation_type"]
        return dataset_related_item
