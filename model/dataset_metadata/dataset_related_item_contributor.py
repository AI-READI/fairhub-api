import uuid
from ..db import db


class DatasetRelatedItemContributor(db.Model):
    def __init__(self):
        self.id = str(uuid.uuid4())

    __tablename__ = "dataset_related_item_contributor"
    id = db.Column(db.CHAR(36), primary_key=True)
    name = db.Column(db.String, nullable=False)
    name_type = db.Column(db.String, nullable=False)
    creator = db.Column(db.BOOLEAN, nullable=False)
    contributor_type = db.Column(db.String, nullable=False)

    dataset_related_item_id = db.Column(
        db.CHAR(36), db.ForeignKey("dataset_related_item.id")
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
        }

    @staticmethod
    def from_data(data: dict):
        dataset_related_contributor = DatasetRelatedItemContributor()
        dataset_related_contributor.name = data["name"]
        dataset_related_contributor.name_type = data["name_type"]
        dataset_related_contributor.creator = data["creator"]
        dataset_related_contributor.contributor_type = data["contributor_type"]
        return dataset_related_contributor
