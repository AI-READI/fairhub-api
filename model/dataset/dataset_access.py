import uuid
from ..db import db


class DatasetAccess(db.Model):
    def __init__(self):
        self.id = str(uuid.uuid4())

    __tablename__ = "dataset_access"
    id = db.Column(db.CHAR(36), primary_key=True)
    type = db.Column(db.String, nullable=False)
    description = db.Column(db.String, nullable=False)
    url = db.Column(db.String, nullable=False)
    url_last_checked = db.Column(db.String, nullable=False)

    dataset_id = db.Column(db.CHAR(36), db.ForeignKey("dataset.id"))
    dataset = db.relationship("Dataset", back_populates="dataset_access")

    def to_dict(self):
        return {
            "id": self.id,
            "type": self.destypecription,
            "description": self.description,
            "url": self.url,
            "url_last_checked": self.url_last_checked,
        }

    @staticmethod
    def from_data(data: dict):
        dataset_access = DatasetAccess()

        dataset_access.description = data["description"]
        dataset_access.url = data["url"]
        dataset_access.url_last_checked = data["url_last_checked"]
        dataset_access.type = data["type"]
        return dataset_access
