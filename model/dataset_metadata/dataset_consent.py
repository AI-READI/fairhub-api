from ..db import db


class DatasetConsent(db.Model):  # type: ignore
    def __init__(self, dataset):
        self.dataset = dataset
        self.type = None
        self.noncommercial = True
        self.geog_restrict = True
        self.research_type = True
        self.genetic_only = True
        self.no_methods = True
        self.details = ""

    __tablename__ = "dataset_consent"

    type = db.Column(db.String, nullable=True)
    noncommercial = db.Column(db.BOOLEAN, nullable=False)
    geog_restrict = db.Column(db.BOOLEAN, nullable=False)
    research_type = db.Column(db.BOOLEAN, nullable=False)
    genetic_only = db.Column(db.BOOLEAN, nullable=False)
    no_methods = db.Column(db.BOOLEAN, nullable=False)
    details = db.Column(db.String, nullable=False)

    dataset_id = db.Column(
        db.CHAR(36), db.ForeignKey("dataset.id"), primary_key=True, nullable=False
    )
    dataset = db.relationship("Dataset", back_populates="dataset_consent")

    def to_dict(self):
        return {
            "type": self.type,
            "noncommercial": self.noncommercial,
            "geog_restrict": self.geog_restrict,
            "research_type": self.research_type,
            "genetic_only": self.genetic_only,
            "no_methods": self.no_methods,
            "details": self.details,
        }

    @staticmethod
    def from_data(dataset, data: dict):
        dataset_consent = DatasetConsent(dataset)
        dataset_consent.update(data)
        return dataset_consent

    def update(self, data: dict):
        self.type = data["type"]
        self.noncommercial = data["noncommercial"]
        self.geog_restrict = data["geog_restrict"]
        self.research_type = data["research_type"]
        self.genetic_only = data["genetic_only"]
        self.no_methods = data["no_methods"]
        self.details = data["details"]
