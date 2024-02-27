from ..db import db


class DatasetHealthsheet(db.Model):  # type: ignore
    def __init__(self, dataset):
        self.dataset = dataset
        self.motivation = "[]"
        self.composition = "[]"
        self.collection = "[]"
        self.preprocessing = "[]"
        self.uses = "[]"
        self.distribution = "[]"
        self.maintenance = "[]"

    __tablename__ = "dataset_healthsheet"

    motivation = db.Column(db.JSON, nullable=False)
    composition = db.Column(db.JSON, nullable=False)
    collection = db.Column(db.JSON, nullable=False)
    preprocessing = db.Column(db.JSON, nullable=False)
    uses = db.Column(db.JSON, nullable=False)
    distribution = db.Column(db.JSON, nullable=False)
    maintenance = db.Column(db.JSON, nullable=False)

    dataset_id = db.Column(
        db.CHAR(36), db.ForeignKey("dataset.id"), primary_key=True, nullable=False
    )
    dataset = db.relationship("Dataset", back_populates="dataset_healthsheet")

    def to_dict(self):
        return {
            "motivation": self.motivation,
            "composition": self.composition,
            "collection": self.collection,
            "preprocessing": self.preprocessing,
            "uses": self.uses,
            "distribution": self.distribution,
            "maintenance": self.maintenance,
            "dataset_id": self.dataset_id,
        }

    @staticmethod
    def from_data(dataset, data: dict):
        dataset_healthsheet = DatasetHealthsheet(dataset)
        dataset_healthsheet.update(data)
        return dataset_healthsheet

    def update(self, data: dict):
        if "motivation" in data:
            self.motivation = data["motivation"]
        if "composition" in data:
            self.composition = data["composition"]
        if "collection" in data:
            self.collection = data["collection"]
        if "preprocessing" in data:
            self.preprocessing = data["preprocessing"]
        if "uses" in data:
            self.uses = data["uses"]
        if "distribution" in data:
            self.distribution = data["distribution"]
        if "maintenance" in data:
            self.maintenance = data["maintenance"]
