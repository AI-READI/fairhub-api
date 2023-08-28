import uuid

from datetime import datetime
from sqlalchemy.sql.expression import true

import model

from .db import db


class Dataset(db.Model):
    def __init__(self, study):
        self.study = study
        self.id = str(uuid.uuid4())
        self.created_at = datetime.now()

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

    dataset_access = db.relationship("DatasetAccess", back_populates="dataset")
    dataset_consent = db.relationship("DatasetConsent", back_populates="dataset")
    dataset_date = db.relationship("DatasetDate", back_populates="dataset")
    dataset_de_ident_level = db.relationship(
        "DatasetDeIdentLevel", back_populates="dataset"
    )
    dataset_description = db.relationship(
        "DatasetDescription", back_populates="dataset"
    )

    dataset_funder = db.relationship("DatasetFunder", back_populates="dataset")
    dataset_alternate_identifier = db.relationship("DatasetAlternateIdentifier", back_populates="dataset")
    dataset_managing_organization = db.relationship(
        "DatasetManagingOrganization", back_populates="dataset"
    )
    dataset_other = db.relationship("DatasetOther", back_populates="dataset")
    dataset_readme = db.relationship("DatasetReadme", back_populates="dataset")
    dataset_record_keys = db.relationship("DatasetRecordKeys", back_populates="dataset")
    dataset_related_item = db.relationship(
        "DatasetRelatedItem", back_populates="dataset"
    )
    dataset_rights = db.relationship("DatasetRights", back_populates="dataset")
    dataset_subject = db.relationship("DatasetSubject", back_populates="dataset")
    dataset_title = db.relationship("DatasetTitle", back_populates="dataset")

    def to_dict(self):
        last_published = self.last_published()
        # last_modified = self.last_modified()

        return {
            "id": self.id,
            "updated_on": str(datetime.now()),
            "created_at": str(datetime.now()),
            # "dataset_versions": [i.to_dict() for i in self.dataset_versions],
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
    def from_data(study, data: dict):
        dataset_obj = Dataset(study)
        dataset_obj.update(data)
        return dataset_obj

    def update(self, data: dict):
        """Creates a new dataset from a dictionary"""
        self.updated_on = datetime.now()
        # self.dataset_versions = data["dataset_versions"]
