import uuid
from ..db import db


class DatasetDeIdentLevel(db.Model):
    def __init__(self):
        self.id = str(uuid.uuid4())

    __tablename__ = "dataset_de_ident_level"
    id = db.Column(db.CHAR(36), primary_key=True)

    type = db.Column(db.String, nullable=False)
    direct = db.Column(db.BOOLEAN, nullable=False)
    hipaa = db.Column(db.BOOLEAN, nullable=False)
    dates = db.Column(db.BOOLEAN, nullable=False)
    nonarr = db.Column(db.BOOLEAN, nullable=False)
    k_anon = db.Column(db.BOOLEAN, nullable=False)
    details = db.Column(db.String, nullable=False)

    dataset_id = db.Column(db.CHAR(36), db.ForeignKey("dataset.id"))
    dataset = db.relationship("Dataset", back_populates="dataset_de_ident_level")

    def to_dict(self):
        return {
            "id": self.id,
            "type": self.type,
            "direct": self.direct,
            "hipaa": self.hipaa,
            "dates": self.dates,
            "nonarr": self.nonarr,
            "k_anon": self.k_anon,
            "details": self.details,
        }

    @staticmethod
    def from_data(data: dict):
        dataset_de_ident_level = DatasetDeIdentLevel()
        dataset_de_ident_level.type = data["type"]
        dataset_de_ident_level.direct = data["direct"]
        dataset_de_ident_level.hipaa = data["hipaa"]
        dataset_de_ident_level.dates = data["dates"]
        dataset_de_ident_level.nonarr = data["nonarr"]
        dataset_de_ident_level.k_anon = data["k_anon"]
        dataset_de_ident_level.details = data["details"]

        return dataset_de_ident_level
