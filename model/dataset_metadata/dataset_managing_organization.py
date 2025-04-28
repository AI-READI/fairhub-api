from ..db import db


class DatasetManagingOrganization(db.Model):  # type: ignore
    def __init__(self, dataset):
        self.dataset = dataset
        self.name = ""
        self.identifier = ""
        self.identifier_scheme = ""
        self.identifier_scheme_uri = ""

    __tablename__ = "dataset_managing_organization"

    name = db.Column(db.String, nullable=False)
    identifier = db.Column(db.String, nullable=False)
    identifier_scheme = db.Column(db.String, nullable=False)
    identifier_scheme_uri = db.Column(db.String, nullable=False)

    dataset_id = db.Column(
        db.CHAR(36), db.ForeignKey("dataset.id"), primary_key=True, nullable=False
    )
    dataset = db.relationship("Dataset", back_populates="dataset_managing_organization")

    def to_dict(self):
        return {
            "name": self.name,
            "identifier": self.identifier,
            "identifier_scheme": self.identifier_scheme,
            "identifier_scheme_uri": self.identifier_scheme_uri,
        }

    def to_dict_metadata(self):
        return {
            "name": self.name,
            "identifier": self.identifier,
        }

    def to_dict_validation(self):
        return {
            "name": self.name,
            "identifier": {
                "value": self.identifier,
                "parent" : self.identifier_scheme
            },
            "identifier_scheme": {
                "value": self.identifier_scheme,
                "parent": self.identifier,
            },
        }

    def validate(self):
        data = self.to_dict_validation()
        invalid_keys = []
        for key, value in data.items():
            if isinstance(value, dict):
                if value["parent"] is None or (
                    isinstance(value, str) and value.strip() != ""
                ):
                    continue  # skip to next loop
            if (
                value is None
                or (isinstance(value, str) and value.strip() == "")
                or (isinstance(value, list) and len(value) == 0)
            ):
                invalid_keys.append(
                    {"metadata_header": "managing organization", "name": key, "route": "team"}
                )
        return invalid_keys

    @staticmethod
    def from_data(dataset, data: dict):
        dataset_other = DatasetManagingOrganization(dataset)
        dataset_other.update(data)
        return dataset_other

    def update(self, data: dict):
        if "name" in data:
            self.name = data["name"]
        if "identifier" in data:
            self.identifier = data["identifier"]
        if "identifier_scheme" in data:
            self.identifier_scheme = data["identifier_scheme"]
        if "identifier_scheme_uri" in data:
            self.identifier_scheme_uri = data["identifier_scheme_uri"]
