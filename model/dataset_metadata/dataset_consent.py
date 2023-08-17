import uuid
from ..db import db


class DatasetConsent(db.Model):
    def __init__(self):
        self.id = str(uuid.uuid4())

    __tablename__ = "dataset_consent"
    id = db.Column(db.CHAR(36), primary_key=True)

    type = db.Column(db.String, nullable=False)
    noncommercial = db.Column(db.BOOLEAN, nullable=False)
    geog_restrict = db.Column(db.BOOLEAN, nullable=False)
    research_type = db.Column(db.BOOLEAN, nullable=False)
    genetic_only = db.Column(db.BOOLEAN, nullable=False)
    no_methods = db.Column(db.BOOLEAN, nullable=False)
    details = db.Column(db.String, nullable=False)

    dataset_id = db.Column(db.CHAR(36), db.ForeignKey("dataset.id"))
    dataset = db.relationship("Dataset", back_populates="dataset_consent")

    def to_dict(self):
        return {
            "id": self.id,
            "type": self.destypecription,
            "noncommercial": self.noncommercial,
            "geog_restrict": self.geog_restrict,
            "research_type": self.research_type,
            "genetic_only": self.genetic_only,
            "no_methods": self.no_methods,
            "details": self.details,
        }

    @staticmethod
    def from_data(data: dict):
        dataset_consent = DatasetConsent()
        dataset_consent.type = data["type"]
        dataset_consent.noncommercial = data["noncommercial"]
        dataset_consent.geog_restrict = data["geog_restrict"]
        dataset_consent.research_type = data["research_type"]
        dataset_consent.genetic_only = data["genetic_only"]
        dataset_consent.no_methods = data["no_methods"]
        dataset_consent.details = data["details"]

        return dataset_consent
