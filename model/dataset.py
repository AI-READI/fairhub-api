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
        self.dataset_de_ident_level = model.DatasetDeIdentLevel(self)
        self.dataset_consent = model.DatasetConsent(self)
        self.dataset_healthsheet = model.DatasetHealthsheet(self)
        self.dataset_other = model.DatasetOther(self)
        self.dataset_managing_organization = model.DatasetManagingOrganization(self)

        self.dataset_title.append(model.DatasetTitle(self))
        self.dataset_description.append(model.DatasetDescription(self))

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
    dataset_healthsheet = db.relationship(
        "DatasetHealthsheet",
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
        "DatasetOther", back_populates="dataset", uselist=False, cascade="all, delete"
    )
    dataset_managing_organization = db.relationship(
        "DatasetManagingOrganization",
        back_populates="dataset",
        uselist=False,
        cascade="all, delete",
    )
    dataset_related_identifier = db.relationship(
        "DatasetRelatedIdentifier", back_populates="dataset", cascade="all, delete"
    )
    dataset_rights = db.relationship(
        "DatasetRights", back_populates="dataset", cascade="all, delete"
    )
    dataset_subject = db.relationship(
        "DatasetSubject", back_populates="dataset", cascade="all, delete"
    )
    dataset_title = db.relationship(
        "DatasetTitle", back_populates="dataset", cascade="all, delete"
    )

    def to_dict(self):
        last_published = self.last_published()
        return {
            "id": self.id,
            "created_at": self.created_at,
            # "dataset_versions": [i.to_dict() for i in self.dataset_versions],
            "latest_version": last_published.id if last_published else None,
            "title": [
                i.title if i.title else None for i in self.dataset_title  # type: ignore
            ][0],
            "description": [
                i.description if i.type == "Abstract" else None
                for i in self.dataset_description  # type: ignore
            ][0],
        }

    def to_dict_dataset_metadata(self):
        return {
            "contributors": [
                i.to_dict_metadata()
                for i in self.dataset_contributors  # type: ignore
                if not i.creator
            ],
            "about": self.dataset_other.to_dict_metadata(),
            "managing_organization": self.dataset_managing_organization.to_dict_metadata(),  # type: ignore
            "access": self.dataset_access.to_dict_metadata(),
            "consent": self.dataset_consent.to_dict_metadata(),
            "dates": [i.to_dict_metadata() for i in self.dataset_date],  # type: ignore
            "de_identification": self.dataset_de_ident_level.to_dict_metadata(),
            "descriptions": [
                i.to_dict_metadata() for i in self.dataset_description  # type: ignore
            ],
            "funders": [
                i.to_dict_metadata() for i in self.dataset_funder  # type: ignore
            ],
            "identifiers": [
                i.to_dict_metadata()
                for i in self.dataset_alternate_identifier  # type: ignore
            ],
            "creators": [
                i.to_dict_metadata()
                for i in self.dataset_contributors  # type: ignore
                if i.creator
            ],
            "related_identifier": [
                i.to_dict_metadata()
                for i in self.dataset_related_identifier  # type: ignore
            ],
            "rights": [
                i.to_dict_metadata() for i in self.dataset_rights  # type: ignore
            ],
            "subjects": [
                i.to_dict_metadata() for i in self.dataset_subject  # type: ignore
            ],
            "titles": [
                i.to_dict_metadata() for i in self.dataset_title  # type: ignore
            ],
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

    def touch_dataset(self):
        self.updated_on = datetime.datetime.now(datetime.timezone.utc).timestamp()
