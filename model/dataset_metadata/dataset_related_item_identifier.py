import uuid
import datetime
from datetime import timezone
from ..db import db


class DatasetRelatedItemIdentifier(db.Model):  # type: ignore
    def __init__(self):
        self.id = str(uuid.uuid4())
        self.created_at = datetime.datetime.now(timezone.utc).timestamp()

    __tablename__ = "dataset_related_item_identifier"
    id = db.Column(db.CHAR(36), primary_key=True)
    identifier = db.Column(db.String, nullable=False)
    type = db.Column(db.String, nullable=True)
    metadata_scheme = db.Column(db.String, nullable=True)
    scheme_uri = db.Column(db.String, nullable=True)
    scheme_type = db.Column(db.String, nullable=True)
    created_at = db.Column(db.BigInteger, nullable=False)

    dataset_related_item_id = db.Column(
        db.CHAR(36), db.ForeignKey("dataset_related_item.id"), nullable=False
    )
    dataset_related_item = db.relationship(
        "DatasetRelatedItem", back_populates="dataset_related_item_identifier"
    )

    def to_dict(self):
        return {
            "id": self.id,
            "identifier": self.identifier,
            "type": self.type,
            "metadata_scheme": self.metadata_scheme,
            "scheme_uri": self.scheme_uri,
            "scheme_type": self.scheme_type,
            "created_at": self.created_at

        }

    @staticmethod
    def from_data(data: dict):
        dataset_related_item_identifier = DatasetRelatedItemIdentifier()
        dataset_related_item_identifier.identifier = data["identifier"]
        dataset_related_item_identifier.type = data["type"]
        dataset_related_item_identifier.metadata_scheme = data["metadata_scheme"]
        dataset_related_item_identifier.scheme_uri = data["scheme_uri"]
        dataset_related_item_identifier.scheme_type = data["scheme_type"]
        return dataset_related_item_identifier
