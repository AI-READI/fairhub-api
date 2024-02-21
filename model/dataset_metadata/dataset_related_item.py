import datetime
import uuid
from datetime import timezone

import model

from ..db import db


class DatasetRelatedItem(db.Model):  # type: ignore
    def __init__(self, dataset):
        self.id = str(uuid.uuid4())
        self.dataset = dataset
        self.created_at = datetime.datetime.now(timezone.utc).timestamp()
        self.dataset_related_item_other = model.DatasetRelatedItemOther(self)

    __tablename__ = "dataset_related_item"

    id = db.Column(db.CHAR(36), primary_key=True)
    type = db.Column(db.String, nullable=True)
    relation_type = db.Column(db.String, nullable=True)
    created_at = db.Column(db.BigInteger, nullable=False)

    dataset_id = db.Column(db.CHAR(36), db.ForeignKey("dataset.id"), nullable=False)
    dataset = db.relationship("Dataset", back_populates="dataset_related_item")

    dataset_related_item_contributor = db.relationship(
        "DatasetRelatedItemContributor",
        back_populates="dataset_related_item",
        cascade="all, delete",
    )
    dataset_related_item_identifier = db.relationship(
        "DatasetRelatedItemIdentifier",
        back_populates="dataset_related_item",
        cascade="all, delete",
    )
    dataset_related_item_other = db.relationship(
        "DatasetRelatedItemOther",
        back_populates="dataset_related_item",
        uselist=False,
        cascade="all, delete",
    )
    dataset_related_item_title = db.relationship(
        "DatasetRelatedItemTitle",
        back_populates="dataset_related_item",
        cascade="all, delete",
    )

    def to_dict(self):
        sorted_contributors = sorted(
            self.dataset_related_item_contributor,
            key=lambda creator: creator.created_at,
        )
        creators = [c for c in sorted_contributors if c.creator]
        contributors = [c for c in sorted_contributors if not c.creator]
        return {
            "id": self.id,
            "type": self.type,
            "relation_type": self.relation_type,
            "created_at": self.created_at,
            "titles": [
                i.to_dict() for i in self.dataset_related_item_title  # type: ignore
            ],
            "creators": [c.to_dict() for c in creators],
            "contributors": [c.to_dict() for c in contributors],
            "publication_year": (
                self.dataset_related_item_other.publication_year
                if self.dataset_related_item_other
                else None
            ),
            "volume": (
                self.dataset_related_item_other.volume
                if self.dataset_related_item_other
                else None
            ),
            "issue": (
                self.dataset_related_item_other.issue
                if self.dataset_related_item_other
                else None
            ),
            "number_value": (
                self.dataset_related_item_other.number_value
                if self.dataset_related_item_other
                else None
            ),
            "number_type": (
                self.dataset_related_item_other.number_type
                if self.dataset_related_item_other
                else None
            ),
            "first_page": (
                self.dataset_related_item_other.first_page
                if self.dataset_related_item_other
                else None
            ),
            "last_page": (
                self.dataset_related_item_other.last_page
                if self.dataset_related_item_other
                else None
            ),
            "publisher": (
                self.dataset_related_item_other.publisher
                if self.dataset_related_item_other
                else None
            ),
            "edition": (
                self.dataset_related_item_other.edition
                if self.dataset_related_item_other
                else None
            ),
            "identifiers": [
                i.to_dict()
                for i in self.dataset_related_item_identifier  # type: ignore
            ],
        }

    def to_dict_metadata(self):
        bigint_timestamp = self.dataset_related_item_other.publication_year
        pub_year = ""
        if bigint_timestamp:
            unix_timestamp = bigint_timestamp / 1000
            datetime_obj = datetime.datetime.utcfromtimestamp(unix_timestamp)
            pub_year = datetime_obj.strftime("%Y")
        sorted_contributors = sorted(
            self.dataset_related_item_contributor,
            key=lambda creator: creator.created_at,
        )

        creators = [c for c in sorted_contributors if c.creator]
        contributors = [c for c in sorted_contributors if not c.creator]
        return {
            "type": self.type,
            "titles": [
                i.to_dict_metadata()
                for i in self.dataset_related_item_title  # type: ignore
            ],
            "identifiers": [
                i.to_dict_metadata()
                for i in self.dataset_related_item_identifier  # type: ignore
            ],
            "creators": [i.to_dict_metadata() for i in creators],  # type: ignore
            "contributors": [
                i.to_dict_metadata() for i in contributors  # type: ignore
            ],
            # "publication_year": self.dataset_related_item_other.publication_year,
            "publication_year": pub_year if bigint_timestamp else None,
            "publisher": self.dataset_related_item_other.publisher,
        }

    @staticmethod
    def from_data(dataset, data: dict):
        dataset_related_item = DatasetRelatedItem(dataset)
        dataset_related_item.update(data)
        return dataset_related_item

    def update(self, data: dict):
        self.type = data["type"]
        self.relation_type = data["relation_type"]
        self.dataset_related_item_other.update(data)
        self.dataset.touch_dataset()
