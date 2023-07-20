from sqlalchemy import String
from datetime import datetime

from sqlalchemy.dialects.postgresql import ARRAY
from sqlalchemy.orm import composite

from .db import db
from .owner import Owner
from .study_contributor import StudyContributor


class Study(db.Model):
    __tablename__ = "study"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String, nullable=False)
    description = db.Column(db.String, nullable=False)
    image = db.Column(db.String, nullable=False)
    keywords = db.Column(ARRAY(String), nullable=False)
    lastUpdated = db.Column(db.DateTime, nullable=False)
    owner = composite(
        Owner,
        db.Column("owner_ORCID", db.String(128), nullable=False),
        db.Column("owner_email", db.String(128), nullable=False),
        db.Column("owner_name", db.String(128), nullable=False),
    )

    contributors = db.relationship("StudyContributor", back_populates="study")
    dataset = db.relationship("Dataset", back_populates="study")

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "image": self.image,
            "keywords": self.keywords,
            "lastUpdated": self.lastUpdated,
            "owner": self.owner.to_dict(),
            "contributors": [
                contributor.to_dict() for contributor in self.contributors
            ],
        }
        # print(json.dumps(list(properties.keys()), indent=4))
        # exit()

    @staticmethod
    def from_data(data):
        study = Study()
        study.update(data)

        return study

    def update(self, data):
        self.title = data["title"]
        self.description = data["description"]
        self.image = data["image"]
        self.keywords = data["keywords"]
        self.lastUpdated = datetime.now()
        self.owner = Owner.from_data(data["owner"])
        self.contributors = [
            StudyContributor.from_data(c) for c in data["contributors"]
        ]

    def validate(self):
        violations = []
        # if self.description.trim() == "":
        #     violations.push("A description is required")
        # if self.keywords.length < 1:
        #     violations.push("At least one keyword must be specified")
        return violations
