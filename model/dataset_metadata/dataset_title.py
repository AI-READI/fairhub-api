import uuid
from ..db import db


class DatasetTitle(db.Model):
    def __init__(self):
        self.id = str(uuid.uuid4())

    __tablename__ = "dataset_title"
    id = db.Column(db.CHAR(36), primary_key=True)
    title = db.Column(db.String, nullable=False)
    type = db.Column(db.String, nullable=False)
    dataset = db.relationship("Dataset", back_populates="dataset_title")
    dataset_id = db.Column(db.String, db.ForeignKey("dataset.id"))

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "type": self.type,
        }

    @staticmethod
    def from_data(data: dict):
        dataset_title = DatasetTitle()

        dataset_title.title = data["title"]
        dataset_title.type = data["type"]
        return dataset_title
