from sqlalchemy.sql.expression import true
import uuid
import model

from .db import db


class Dataset(db.Model):
    def __init__(self, study):
        self.study = study
        self.id = str(uuid.uuid4())

    __tablename__ = "dataset"
    id = db.Column(db.CHAR(36), primary_key=True)

    study_id = db.Column(db.CHAR(36), db.ForeignKey("study.id"))
    study = db.relationship("Study", back_populates="dataset")
    dataset_versions = db.relationship(
        "DatasetVersion", back_populates="dataset", lazy="dynamic"
    )

    def to_dict(self):
        last_published = self.last_published()
        last_modified = self.last_modified()
        return (
            model.DatasetVersions(
                last_published,
                last_modified,
                last_published.name if last_published else last_modified.name,
                self.id,
            )
        ).to_dict()

    def last_published(self):
        return (
            self.dataset_versions.filter(model.DatasetVersion.published == true())
            .order_by(model.DatasetVersion.published.desc())
            .first()
        )

    def last_modified(self):
        return self.dataset_versions.order_by(
            model.DatasetVersion.modified.desc()
        ).first()

    @staticmethod
    def from_data(data):
        dataset = Dataset()
        # dataset.id = data["id"]
        for i in data.values():
            print(i)
        return dataset
