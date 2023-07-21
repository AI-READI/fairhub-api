from flask import Blueprint, jsonify, request

# from faker import Faker
from model import Participant, db

participant = Blueprint("participant", __name__)


@participant.route("/study/<studyId>/participants", methods=["GET"])
def get_participants(studyId):
    # fake = Faker()
    # data = [
    #     {
    #         "participant_id": _ + 1,
    #         "name": fake.name(),
    #         "address": fake.street_address(),
    #         "age": fake.random_int(min=1, max=99),
    #     }
    #     for _ in range(30)
    # ]
    participants = Participant.query.all()
    return jsonify([p.to_dict() for p in participants])


@participant.route("/study/<studyId>/participants/add", methods=["POST"])
def add_participants(studyId):
    addParticipant = Participant.from_data(request.json)
    db.session.add(addParticipant)
    db.session.commit()
    return jsonify(addParticipant.to_dict()), 201


# in progress update participants
@participant.route("/study/<studyId>/participants/update", methods=["POST"])
def update_participants(studyId):
    updateParticipant = Participant.query.get(studyId)
    # if not addStudy.validate():
    #     return 'error', 422
    updateParticipant.update(request.json)
    db.session.commit()
    return jsonify(updateParticipant.to_dict()), 201
