from . import db
import model
from sqlalchemy.sql.expression import true
class Dataset(db.Model):
    __tablename__ = "dataset"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)

    study_id = db.Column(db.Integer, db.ForeignKey("study.id"))
    study = db.relationship("Study", back_populates="dataset")
    datasetVersions = db.relationship("DatasetVersion", back_populates="dataset", lazy="dynamic")

    def to_dict(self):
        lastPublished = self.lastPublished()
        return (model.DatasetVersions(lastPublished, self.lastModified(), lastPublished.name, self.id)).to_dict()

    def lastPublished(self):
        return self.datasetVersions.filter(model.DatasetVersion.published == true()).order_by(
            model.DatasetVersion.modified.desc()).first()
    def lastModified(self):
        return self.datasetVersions.order_by(model.DatasetVersion.modified.desc()).first()
