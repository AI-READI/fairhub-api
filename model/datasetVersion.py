from .db import db
from .version_contributor import VersionContributor


class DatasetVersion(db.Model):
    def __init__(self, dataset):
        self.dataset=dataset
    __tablename__ = "datasetVersion"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String, nullable=False)
    description = db.Column(db.String, nullable=False)
    keywords = db.Column(db.String, nullable=False)
    primaryLanguage = db.Column(db.String, nullable=False)
    selectedParticipants = db.Column(db.String, nullable=False)
    modified = db.Column(db.DateTime, nullable=True)
    published = db.Column(db.Boolean, nullable=False)
    DOI = db.Column(db.String, nullable=False)
    name = db.Column(db.String, nullable=False)
    versionContributors = db.relationship(
        "VersionContributor", back_populates="datasetVersion"
    )

    dataset_id = db.Column(db.Integer, db.ForeignKey("dataset.id"))
    dataset = db.relationship("Dataset", back_populates="datasetVersions")

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "keywords": self.keywords,
            "primaryLanguage": self.primaryLanguage,
            "selectedParticipants": self.selectedParticipants,
            "modified": self.modified,
            "published": self.published,
            "versionContributors": [
                versionContributor.to_dict()
                for versionContributor in self.versionContributors
            ],
            "DOI": self.DOI,
            "name": self.name,
        }
    @staticmethod
    def from_data(dataset, data):
        datasetVersion_obj = DatasetVersion(dataset)
        # datasetVersion_obj.id = data['id']
        datasetVersion_obj.title = data["title"]
        datasetVersion_obj.description = data["description"]
        datasetVersion_obj.keywords = data["keywords"]
        datasetVersion_obj.primaryLanguage = data["primaryLanguage"]
        datasetVersion_obj.selectedParticipants = data["selectedParticipants"]
        datasetVersion_obj.modified = data["modified"]
        datasetVersion_obj.published = data["published"]
        datasetVersion_obj.versionContributors = [
            VersionContributor.from_data(c) for c in data["versionContributors"]
        ]
        datasetVersion_obj.DOI = data["DOI"]
        datasetVersion_obj.name = data["name"]
        return datasetVersion_obj
