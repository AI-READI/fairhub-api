from __main__ import db


class Dataset(db.Model):
    __tablename__ = "dataset"
    id = db.Column(db.Integer, primary_key=True)

    study_id = db.Column(db.Integer, db.ForeignKey("study.id"))
    study = db.relationship("Dataset", back_populates="study")
