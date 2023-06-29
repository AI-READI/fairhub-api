from __main__ import db


class Participant(db.Model):
    __tablename__ = "participant"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    address = db.Column(db.String)
    age = db.Column(db.String)

    study_id = db.Column(db.Integer, db.ForeignKey("study.id"))
    study = db.relationship("Participant")
