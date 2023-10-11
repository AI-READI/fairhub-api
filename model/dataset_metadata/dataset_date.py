import uuid

from ..db import db


class DatasetDate(db.Model):
    def __init__(self, dataset):
        self.id = str(uuid.uuid4())
        self.dataset = dataset

    __tablename__ = "dataset_date"
    id = db.Column(db.CHAR(36), primary_key=True)
    date = db.Column(db.String, nullable=False)
    date_type = db.Column(db.String, nullable=False)
    data_information = db.Column(db.String, nullable=False)

    dataset_id = db.Column(db.CHAR(36), db.ForeignKey("dataset.id"), nullable=False)
    dataset = db.relationship("Dataset", back_populates="dataset_date")

    def to_dict(self):
        return {
            "id": self.id,
            "date": self.date,
            "date_type": self.date_type,
            "data_information": self.data_information,
        }

    @staticmethod
    def from_data(dataset, data: dict):
        dataset_date = DatasetDate(dataset)
        dataset_date.update(data)
        return dataset_date

    def update(self, data):
        self.date = data["date"]
        self.date_type = data["date_type"]
        self.data_information = data["data_information"]
