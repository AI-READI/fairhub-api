from .db import db


class VersionReadme(db.Model):  # type: ignore
    __tablename__ = "version_readme"
    content = db.Column(db.String, nullable=True)

    version_id = db.Column(
        db.CHAR(36), db.ForeignKey("version.id"), primary_key=True, nullable=False
    )
    version = db.relationship("Version", back_populates="version_readme")

    def to_dict(self):
        return {
            "content": self.content,
        }

    @staticmethod
    def from_data(data: dict):
        user = VersionReadme()
        user.update(data)
        return user

    def update(self, data: dict):
        self.content = data["content"]
