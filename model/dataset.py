from . import db


class Dataset(db.Model):
    __tablename__ = "dataset"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)

    study_id = db.Column(db.Integer, db.ForeignKey("study.id"))
    study = db.relationship("Study", back_populates="datasets")

    def to_dict(self):
        return \
            {
                "id": self.id,
            }