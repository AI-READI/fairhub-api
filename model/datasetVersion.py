from __main__ import db


class DatasetVersion(db.Model):
    __tablename__ = 'datasetVersion'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String)
    description = db.Column(db.String)
    keywords = db.Column(db.String)
    primaryLanguage = db.Column(db.String)
    selectedParticipants = db.Column(db.String)

    versionContributor = db.relationship("DatasetVersion", back_populates="versionContributor")

    dataset_id = db.Column(db.Integer, db.ForeignKey("dataset.id"))
    dataset = db.relationship("DatasetVersion", back_populates="dataset")


