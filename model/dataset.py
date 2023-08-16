import uuid

from datetime import datetime
from sqlalchemy.sql.expression import true

import model

from .db import db


class Dataset(db.Model):
    def __init__(self, study):
        self.study = study
        self.id = str(uuid.uuid4())

    __tablename__ = "dataset"
    id = db.Column(db.CHAR(36), primary_key=True)
    updated_on = db.Column(db.DateTime, nullable=False)
    created_at = db.Column(db.DateTime, nullable=False)

    study_id = db.Column(db.CHAR(36), db.ForeignKey("study.id"))
    study = db.relationship("Study", back_populates="dataset")

    dataset_contributors = db.relationship(
        "DatasetContributor", back_populates="dataset"
    )
    dataset_versions = db.relationship(
        "DatasetVersion", back_populates="dataset", lazy="dynamic"
    )

    def to_dict(self):
        last_published = self.last_published()
        last_modified = self.last_modified()

        return {
            "id": self.id,
            "updated_on": str(datetime.now()),
            "created_at": str(datetime.now()),
            "dataset_versions": [i.to_dict() for i in self.dataset_versions],
            "latest_version": last_published.id if last_published else None,
        }

    def last_published(self):
        return (
            self.dataset_versions.filter(model.DatasetVersion.published == true())
            .order_by(model.DatasetVersion.published_on.desc())
            .first()
        )

    def last_modified(self):
        return self.dataset_versions.order_by(
            model.DatasetVersion.updated_on.desc()
        ).first()

    @staticmethod
    def from_data(data: dict):
        """Creates a new dataset from a dictionary"""
        dataset = Dataset()
        dataset.latest_version = data["latest_version"]
        dataset.published_year = data["published_year"]
        dataset.resource_type = data["resource_type"]
        dataset.publisher = data["publisher"]
        dataset.primary_language = data["primary_language"]
        dataset.keywords = data["keywords"]

        return dataset
