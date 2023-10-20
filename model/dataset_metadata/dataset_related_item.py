import datetime
import uuid
from datetime import timezone


from ..db import db


class DatasetRelatedItem(db.Model):  # type: ignore
    def __init__(self, dataset):
        self.id = str(uuid.uuid4())
        self.dataset = dataset
        self.created_at = datetime.datetime.now(timezone.utc).timestamp()
        # self.dataset_related_item_other = model.DatasetRelatedItemOther(self)

    __tablename__ = "dataset_related_item"

    id = db.Column(db.CHAR(36), primary_key=True)
    type = db.Column(db.String, nullable=True)
    relation_type = db.Column(db.String, nullable=True)
    created_at = db.Column(db.BigInteger, nullable=False)

    dataset_id = db.Column(db.CHAR(36), db.ForeignKey("dataset.id"), nullable=False)
    dataset = db.relationship("Dataset", back_populates="dataset_related_item")

    dataset_related_item_contributor = db.relationship(
        "DatasetRelatedItemContributor", back_populates="dataset_related_item"
    )
    dataset_related_item_identifier = db.relationship(
        "DatasetRelatedItemIdentifier", back_populates="dataset_related_item"
    )
    dataset_related_item_other = db.relationship(
        "DatasetRelatedItemOther", back_populates="dataset_related_item", uselist=False
    )
    dataset_related_item_title = db.relationship(
        "DatasetRelatedItemTitle", back_populates="dataset_related_item"
    )

    def to_dict(self):
        sorted_contributors = sorted(
            self.dataset_related_item_contributor,
            key=lambda creator: creator.created_at,
        )
        creators = [creator for creator in sorted_contributors if creator.creator]

        contributors = [
            contributor for contributor in sorted_contributors if not contributor.creator]

        return {
            "id": self.id,
            "type": self.type,
            "relation_type": self.relation_type,
            "created_at": self.created_at,
            "titles": [i.to_dict() for i in self.dataset_related_item_title],
            "creators": [c.to_dict() for c in creators],
            "contributors": [c.to_dict() for c in contributors],
            "identifiers": [i.to_dict() for i in self.dataset_related_item_identifier]
        }

    @staticmethod
    def from_data(dataset, data: dict):
        dataset_related_item = DatasetRelatedItem(dataset)
        dataset_related_item.update(data)
        return dataset_related_item

    def update(self, data: dict):
        self.type = data["type"]
        self.relation_type = data["relation_type"]
