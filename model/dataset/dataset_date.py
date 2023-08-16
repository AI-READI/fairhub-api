import uuid
from ..db import db


class DatasetDate(db.Model):
    def __init__(self):
        self.id = str(uuid.uuid4())

    __tablename__ = "dataset_date"
    id = db.Column(db.CHAR(36), primary_key=True)
    date = db.Column(db.String, nullable=False)
    date_type = db.Column(db.String, nullable=False)
    data_information = db.Column(db.String, nullable=False)

    dataset_id = db.Column(db.CHAR(36), db.ForeignKey("dataset.id"))
    dataset = db.relationship("Dataset", back_populates="dataset_date")

    def to_dict(self):
        return {
            "id": self.id,
            "date": self.date,
            "date_type": self.date_type,
            "data_information": self.data_information,
        }

    @staticmethod
    def from_data(data: dict):
        dataset_date = DatasetDate()
        # dataset_contributor.id = data["id"]
        dataset_date.date = data["date"]
        dataset_date.date_type = data["date_type"]
        dataset_date.data_information = data["data_information"]
        return dataset_date
