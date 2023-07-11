from . import db
from .owner import Owner
from sqlalchemy import String
from sqlalchemy.dialects.postgresql import ARRAY
from sqlalchemy.orm import composite
import json

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
    datasets = db.relationship("Dataset", back_populates="study")

    def to_dict(self):
        return \
            {
                "id": self.id,
                "title": self.title,
                "description": self.description,
                "image": self.image,
                "keywords": self.keywords,
                "lastUpdated": self.lastUpdated,
                "owner": self.owner.to_dict(),
                "contributors": [contributor.to_dict() for contributor in self.contributors]
            }
        # print(json.dumps(list(properties.keys()), indent=4))
        # exit()



