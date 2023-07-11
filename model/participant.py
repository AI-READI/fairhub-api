from . import db


class Participant(db.Model):
    __tablename__ = "participant"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String, nullable=False)
    address = db.Column(db.String, nullable=False)
    age = db.Column(db.String, nullable=False)

    study_id = db.Column(db.Integer, db.ForeignKey("study.id"))
    study = db.relationship("Study")

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "address": self.address,
            "age": self.age,
        }
