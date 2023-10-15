from ..db import db


class DatasetDeIdentLevel(db.Model):  # type: ignore
    def __init__(self, dataset):
        self.dataset = dataset
        self.type = None
        self.direct = False
        self.hipaa = False
        self.dates = False
        self.nonarr = False
        self.k_anon = False
        self.details = False

    __tablename__ = "dataset_de_ident_level"

    type = db.Column(db.String, nullable=True)
    direct = db.Column(db.BOOLEAN, nullable=False)
    hipaa = db.Column(db.BOOLEAN, nullable=False)
    dates = db.Column(db.BOOLEAN, nullable=False)
    nonarr = db.Column(db.BOOLEAN, nullable=False)
    k_anon = db.Column(db.BOOLEAN, nullable=False)
    details = db.Column(db.String, nullable=False)

    dataset_id = db.Column(db.CHAR(36), db.ForeignKey("dataset.id"), primary_key=True, nullable=False)
    dataset = db.relationship("Dataset", back_populates="dataset_de_ident_level")

    def to_dict(self):
        return {
            "type": self.type,
            "direct": self.direct,
            "hipaa": self.hipaa,
            "dates": self.dates,
            "nonarr": self.nonarr,
            "k_anon": self.k_anon,
            "details": self.details,
        }

    @staticmethod
    def from_data(dataset, data: dict):
        dataset_de_ident_level = DatasetDeIdentLevel(dataset)
        dataset_de_ident_level.update(data)
        return dataset_de_ident_level

    def update(self, data: dict):
        self.type = data["type"]
        self.direct = data["direct"]
        self.hipaa = data["hipaa"]
        self.dates = data["dates"]
        self.nonarr = data["nonarr"]
        self.k_anon = data["k_anon"]
        self.details = data["details"]
