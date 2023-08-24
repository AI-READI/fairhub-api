import uuid
from ..db import db


class DatasetSubject(db.Model):
    def __init__(self, dataset):
        self.id = str(uuid.uuid4())
        self.dataset = dataset
    __tablename__ = "dataset_subject"
    id = db.Column(db.CHAR(36), primary_key=True)

    subject = db.Column(db.String, nullable=False)
    scheme = db.Column(db.String, nullable=False)
    scheme_uri = db.Column(db.String, nullable=False)
    value_uri = db.Column(db.String, nullable=False)
    classification_code = db.Column(db.String, nullable=False)

    dataset_id = db.Column(db.CHAR(36), db.ForeignKey("dataset.id"))
    dataset = db.relationship("Dataset", back_populates="dataset_subject")

    def to_dict(self):
        return {
            "id": self.id,
            "subject": self.subject,
            "scheme": self.scheme,
            "scheme_uri": self.scheme_uri,
            "value_uri": self.value_uri,
            "classification_code": self.classification_code,
        }

    @staticmethod
    def from_data(dataset, data: dict):
        dataset_subject = DatasetSubject(dataset)
        dataset_subject.update(data)
        return dataset_subject

    def update(self, data):
        self.subject = data["subject"]
        self.scheme = data["scheme"]
        self.scheme_uri = data["scheme_uri"]
        self.value_uri = data["value_uri"]
        self.classification_code = data["classification_code"]
