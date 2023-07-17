from .db import db


class DatasetVersion(db.Model):
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
            "versionContributors": [
                versionContributor.to_dict()
                for versionContributor in self.versionContributors
            ],
            "DOI": self.DOI,
            "name": self.name,
        }
