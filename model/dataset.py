from sqlalchemy.sql.expression import true

import model

from .db import db


class Dataset(db.Model):
    def __init__(self, study):
        self.study = study
    __tablename__ = "dataset"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)

    study_id = db.Column(db.Integer, db.ForeignKey("study.id"))
    study = db.relationship("Study", back_populates="dataset")
    datasetVersions = db.relationship(
        "DatasetVersion", back_populates="dataset", lazy="dynamic"
    )

    def to_dict(self):
        lastPublished = self.lastPublished()
        lastModified = self.lastModified()
        return (
            model.DatasetVersions(
                lastPublished, lastModified, lastPublished.name if lastPublished else lastModified.name, self.id
            )
        ).to_dict()

    def lastPublished(self):
        return (
            self.datasetVersions.filter(model.DatasetVersion.published == true())
            .order_by(model.DatasetVersion.published.desc())
            .first()
        )

    def lastModified(self):
        return self.datasetVersions.order_by(
            model.DatasetVersion.modified.desc()
        ).first()

    @staticmethod
    def from_data(data):
        dataset = Dataset()
        # dataset.id = data["id"]
        return dataset
