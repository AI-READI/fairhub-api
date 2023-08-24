import uuid
from ..db import db


class DatasetReadme(db.Model):
    def __init__(self, dataset):
        self.id = str(uuid.uuid4())
        self.dataset = dataset
    __tablename__ = "dataset_readme"
    id = db.Column(db.CHAR(36), primary_key=True)
    content = db.Column(db.String, nullable=False)

    dataset_id = db.Column(db.CHAR(36), db.ForeignKey("dataset.id"))
    dataset = db.relationship("Dataset", back_populates="dataset_readme")

    def to_dict(self):
        return {
            "id": self.id,
            "content": self.content,
        }

    @staticmethod
    def from_data(dataset, data: dict):
        dataset_readme = DatasetReadme(dataset)
        dataset_readme.update(data)
        return dataset_readme

    def update(self, data):
        self.content = data["content"]


