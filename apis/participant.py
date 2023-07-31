from flask import Blueprint, jsonify, request, Response
from model import Participant, db, Study

participant = Blueprint("participant", __name__)


# @participant.route("/study/<study_id>/participants", methods=["GET"])
# def get_participants(study_id):
#     participants = Participant.query.all()
#     return jsonify([p.to_dict() for p in participants])
#

# @participant.route("/study/<study_id>/participants/add", methods=["POST"])
# def add_participants(study_id):
#     study = Study.query.get(study_id)
#     add_participant = Participant.from_data(request.json, study)
#     db.session.add(add_participant)
#     db.session.commit()
#     return jsonify(add_participant.to_dict()), 201


# in progress update participants
# @participant.route("/study/<study_id>/participants/<participant_id>", methods=["PUT"])
# def update_participants(study_id, participant_id):
#     update_participant = Participant.query.get(participant_id)
#     update_participant.update(request.json)
#     db.session.commit()
#     return jsonify(update_participant.to_dict()), 200
#
#
# @participant.route("/study/<study_id>/participants/<participant_id>", methods=["DELETE"])
# def delete_participants(study_id, participant_id):
#     delete_participant = Participant.query.get(participant_id)
#     db.session.delete(delete_participant)
#     db.session.commit()
#     return Response(status=204)
