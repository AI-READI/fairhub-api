from .db import db
import uuid


version_contributors = db.Table(
    "version_contributors",
    db.Model.metadata,
    db.Column(
        "dataset_version_id", db.ForeignKey("dataset_version.id"), primary_key=True
    ),
    db.Column("user_id", db.ForeignKey("user.id"), primary_key=True),
)


version_participants = db.Table(
    "version_participants",
    db.Model.metadata,
    db.Column(
        "dataset_version_id", db.ForeignKey("dataset_version.id"), primary_key=True
    ),
    db.Column("participant_id", db.ForeignKey("participant.id"), primary_key=True),
)


class DatasetVersion(db.Model):
    def __init__(self, dataset):
        self.dataset = dataset
        self.id = str(uuid.uuid4())

    __tablename__ = "dataset_version"
    id = db.Column(db.CHAR(36), primary_key=True)
    title = db.Column(db.String, nullable=False)
    description = db.Column(db.String, nullable=False)
    keywords = db.Column(db.String, nullable=False)
    primary_language = db.Column(db.String, nullable=False)
    selected_participants = db.Column(db.String, nullable=False)
    modified = db.Column(db.DateTime, nullable=True)
    published = db.Column(db.Boolean, nullable=False)
    DOI = db.Column(db.String, nullable=False)
    name = db.Column(db.String, nullable=False)
    contributors = db.relationship("User", secondary=version_contributors)

    dataset_id = db.Column(db.CHAR(36), db.ForeignKey("dataset.id"))
    dataset = db.relationship("Dataset", back_populates="dataset_versions")
    participants = db.relationship("Participant", secondary=version_participants)

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "keywords": self.keywords,
            "primary_language": self.primary_language,
            "selected_participants": self.selected_participants,
            "modified": self.modified,
            "published": self.published,
            "contributors": [user.to_dict() for user in self.contributors],
            "DOI": self.DOI,
            "name": self.name,
        }

    @staticmethod
    def from_data(data, dataset):
        dataset_version_obj = DatasetVersion(dataset)
        dataset_version_obj.update(data)
        # dataset_version_obj.versionContributors = [
        #     VersionContributor.from_data(c) for c in data["versionContributors"]
        # ]
        return dataset_version_obj

    def update(self, data):
        self.title = data["title"]
        self.description = data["description"]
        self.keywords = data["keywords"]
        self.primary_language = data["primary_language"]
        self.selected_participants = data["selected_participants"]
        self.modified = data["modified"]
        self.published = data["published"]

        self.DOI = data["DOI"]
        self.name = data["name"]
