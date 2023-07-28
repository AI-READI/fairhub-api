from sqlalchemy import String
from datetime import datetime
from sqlalchemy.dialects.postgresql import ARRAY
import model
from .db import db

# from .study_contributor import StudyContributor
import uuid


study_contributors = db.Table(
    "study_contributors",
    db.Model.metadata,
    db.Column("study_id", db.ForeignKey("study.id"), primary_key=True),
    db.Column("user_id", db.ForeignKey("user.id"), primary_key=True),
)


class Study(db.Model):
    def __init__(self):
        self.id = str(uuid.uuid4())

    __tablename__ = "study"

    id = db.Column(db.CHAR(36), primary_key=True)
    title = db.Column(db.String, nullable=False)
    description = db.Column(db.String, nullable=False)
    image = db.Column(db.String, nullable=False)
    size = db.Column(db.String, nullable=False)
    keywords = db.Column(ARRAY(String), nullable=False)
    last_updated = db.Column(db.DateTime, nullable=False)
    dataset = db.relationship("Dataset", back_populates="study")

    owner = db.relationship("User")
    owner_id = db.Column(db.CHAR(36), db.ForeignKey("user.id"))
    contributors = db.relationship("User", secondary=study_contributors)
    participants = db.relationship(
        "Participant", back_populates="study")

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "image": self.image,
            "keywords": self.keywords,
            "last_updated": self.last_updated,
            "size": self.size,
            # "contributors": [
            #     contributor.to_dict() for contributor in self.contributors
            # ],
            "owner": self.owner.to_dict(),
        }

    @staticmethod
    def from_data(data):
        study = Study()
        study.update(data)

        return study

    def update(self, data):
        self.title = data["title"]
        self.description = data["description"]
        self.image = data["image"]
        self.size = data["size"]
        self.keywords = data["keywords"]
        self.last_updated = datetime.now()
        self.owner = model.User.from_data(data["owner"])

    def validate(self):
        violations = []
        # if self.description.trim() == "":
        #     violations.push("A description is required")
        # if self.keywords.length < 1:
        #     violations.push("At least one keyword must be specified")
        return violations
