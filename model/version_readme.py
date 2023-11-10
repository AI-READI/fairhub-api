from .db import db


class VersionReadme(db.Model):  # type: ignore
    def __init__(self, version):
        self.version = version
        self.content = ""

    __tablename__ = "version_readme"
    content = db.Column(db.String, nullable=True)

    version_id = db.Column(
        db.CHAR(36), db.ForeignKey("version.id"), primary_key=True, nullable=False
    )
    version = db.relationship("Version", back_populates="version_readme")

    def to_dict(self):
        return {
            "readme": self.content,
        }

    @staticmethod
    def from_data(version, data: dict):
        readme = VersionReadme(version)
        readme.update(data)
        return readme

    def update(self, data: dict):
        self.content = data["readme"]
