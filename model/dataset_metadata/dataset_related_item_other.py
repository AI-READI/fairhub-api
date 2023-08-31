import uuid
from ..db import db


class DatasetRelatedItemOther(db.Model):
    def __init__(self, dataset):
        self.id = str(uuid.uuid4())
        self.dataset = dataset

    __tablename__ = "dataset_related_item_other"
    id = db.Column(db.CHAR(36), primary_key=True)
    publication_year = db.Column(db.String, nullable=False)
    volume = db.Column(db.String, nullable=False)
    issue = db.Column(db.String, nullable=False)
    number_value = db.Column(db.String, nullable=False)
    number_type = db.Column(db.String, nullable=False)
    first_page = db.Column(db.String, nullable=False)
    last_page = db.Column(db.BOOLEAN, nullable=False)
    publisher = db.Column(db.String, nullable=False)
    edition = db.Column(db.String, nullable=False)

    dataset_related_item_id = db.Column(
        db.CHAR(36), db.ForeignKey("dataset_related_item.id")
    )
    dataset_related_item = db.relationship(
        "DatasetRelatedItem", back_populates="dataset_related_item_other"
    )

    def to_dict(self):
        return {
            "id": self.id,
            "publication_year": self.publication_year,
            "volume": self.volume,
            "issue": self.issue,
            "number_value": self.number_value,
            "number_type": self.number_type,
            "first_page": self.first_page,
            "last_page": self.last_page,
            "publisher": self.publisher,
            "edition": self.edition,
            "scheme_type": self.scheme_type,
        }

    @staticmethod
    def from_data(dataset, data: dict):
        dataset_related_item_other = DatasetRelatedItemOther(dataset)
        dataset_related_item_other.update(data)
        return dataset_related_item_other

    def update(self, data):
        self.publication_year = data["publication_year"]
        self.volume = data["volume"]
        self.issue = data["issue"]
        self.number_value = data["number_value"]
        self.number_type = data["number_type"]
        self.first_page = data["first_page"]
        self.last_page = data["last_page"]
        self.publisher = data["publisher"]
        self.edition = data["edition"]