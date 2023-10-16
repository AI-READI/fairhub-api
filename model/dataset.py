import datetime
import uuid
from datetime import timezone

from sqlalchemy.sql.expression import true

import model

from .db import db
from .study import Study


class Dataset(db.Model):  # type: ignore
    def __init__(self, study):
        self.study = study
        self.id = str(uuid.uuid4())
        self.created_at = datetime.datetime.now(timezone.utc).timestamp()

        self.dataset_access = model.DatasetAccess(self)
        self.dataset_record_keys = model.DatasetRecordKeys(self)
        self.dataset_de_ident_level = model.DatasetDeIdentLevel(self)
        self.dataset_consent = model.DatasetConsent(self)
        self.dataset_readme = model.DatasetReadme(self)
        self.dataset_other = model.DatasetOther(self)

    __tablename__ = "dataset"
    id = db.Column(db.CHAR(36), primary_key=True)
    updated_on = db.Column(db.BigInteger, nullable=False)
    created_at = db.Column(db.BigInteger, nullable=False)

    study_id = db.Column(
        db.CHAR(36), db.ForeignKey("study.id", ondelete="CASCADE"), nullable=False
    )
    study = db.relationship("Study", back_populates="dataset")

    dataset_contributors = db.relationship(
        "DatasetContributor",
        back_populates="dataset",
        cascade="all, delete",
    )
    dataset_versions = db.relationship(
        "Version",
        back_populates="dataset",
        lazy="dynamic",
        cascade="all, delete",
    )

    dataset_access = db.relationship(
        "DatasetAccess",
        back_populates="dataset",
        cascade="all, delete",
        uselist=False,
    )
    dataset_consent = db.relationship(
        "DatasetConsent",
        back_populates="dataset",
        cascade="all, delete",
        uselist=False,
    )
    dataset_date = db.relationship(
        "DatasetDate",
        back_populates="dataset",
        cascade="all, delete",
    )
    dataset_de_ident_level = db.relationship(
        "DatasetDeIdentLevel",
        uselist=False,
        back_populates="dataset",
        cascade="all, delete",
    )
    dataset_description = db.relationship(
        "DatasetDescription",
        back_populates="dataset",
        cascade="all, delete",
    )

    dataset_funder = db.relationship(
        "DatasetFunder",
        back_populates="dataset",
        cascade="all, delete",
    )
    dataset_alternate_identifier = db.relationship(
        "DatasetAlternateIdentifier",
        back_populates="dataset",
        cascade="all, delete",
    )
    dataset_other = db.relationship(
        "DatasetOther", back_populates="dataset", uselist=False
    )
    dataset_readme = db.relationship(
        "DatasetReadme", back_populates="dataset", uselist=False
    )
    dataset_record_keys = db.relationship(
        "DatasetRecordKeys", back_populates="dataset", uselist=False
    )
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
            "created_at": self.created_at,
            # "dataset_versions": [i.to_dict() for i in self.dataset_versions],
            "latest_version": last_published.id if last_published else None,
        }

    def last_published(self):
        return (
            self.dataset_versions.filter(model.Version.published == true())
            .order_by(model.Version.published_on.desc())
            .first()
        )

    def last_modified(self):
        return self.dataset_versions.order_by(
            model.Version.updated_on.desc()
        ).first()  # type: ignore

    @staticmethod
    def from_data(study: Study):
        dataset_obj = Dataset(study)
        dataset_obj.update()
        return dataset_obj

    def update(self):
        """Creates a new dataset from a dictionary"""
        self.updated_on = datetime.datetime.now(timezone.utc).timestamp()
        # self.dataset_versions = data["dataset_versions"]
