from .db import db


class Participant(db.Model):
    __tablename__ = "participant"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    firstname = db.Column(db.String, nullable=False)
    lastname = db.Column(db.String, nullable=False)
    address = db.Column(db.String, nullable=False)
    age = db.Column(db.String, nullable=False)

    study_id = db.Column(db.Integer, db.ForeignKey("study.id"))
    study = db.relationship("Study")

    def to_dict(self):
        return {
            "id": self.id,
            "firstname": self.firstname,
            "lastname": self.lastname,
            "address": self.address,
            "age": self.age,
        }

    @staticmethod
    def from_data(data):
        participant = Participant()
        # participant.id = data["id"]
        participant.firstname = data["firstname"]
        participant.lastname = data["lastname"]
        participant.address = data["address"]

        participant.age = data["age"]

        return participant
