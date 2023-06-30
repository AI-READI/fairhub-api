from __main__ import db
from datasetVersion import DatasetVersion
from owner import Owner
from sqlalchemy import String
from sqlalchemy.dialects.postgresql import ARRAY
from sqlalchemy.orm import composite


class Study(db.Model):
    __tablename__ = "study"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    title = db.Column(db.String)
    description = db.Column(db.String, nullable=False)
    image = db.Column(db.String, nullable=False)
    keywords = db.Column(ARRAY(String), nullable=False)
    lastPublished = composite(
        DatasetVersion,
        db.Column("date", String(128)),
        db.Column("doi", String(128)),
        db.Column("version", String(128)),
    )
    lastUpdated = db.Column(db.String)
    owner = composite(
        Owner, db.Column("name", db.String(128)), db.Column("age", String(3))
    )

    contributors = db.relationship("StudyContributor", back_populates="study")
    dataset = db.relationship("Dataset", back_populates="study")
