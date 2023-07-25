from flask import Blueprint, jsonify, request
from model import Participant, db, Study

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
    study = Study.query.get(studyId)
    add_participant = Participant.from_data(request.json, study)
    db.session.add(add_participant)
    db.session.commit()
    return jsonify(add_participant.to_dict()), 201


# in progress update participants
@participant.route("/study/<studyId>/participants/<participantId>", methods=["POST"])
def update_participants(studyId, participant_id):
    update_participant = Participant.query.get(participant_id)
    update_participant.update(request.json)
    db.session.commit()
    return jsonify(update_participant.to_dict()), 200
