from flask import Response, jsonify, request
from flask_restx import Namespace, Resource, fields

from model import Participant, Study, db

api = Namespace("participant", description="participant operations", path="/")

participant_model = api.model(
    "Study",
    {
        "id": fields.String(required=True),
        "first_name": fields.String(required=True),
        "last_name": fields.String(required=True),
        "created_at": fields.String(required=True),
        "updated_on": fields.String(required=True),
        "address": fields.String(required=True),
        "age": fields.String(required=True),
    },
)


@api.route("/study/<study_id>/participants")
class AddParticipant(Resource):
    @api.doc("participants")
    @api.response(200, "Success")
    @api.response(400, "Validation Error")
    @api.param("id", "Adding participants")
    @api.marshal_with(participant_model)
    def get(self, study_id: int):
        participants = Participant.query.all()
        return [p.to_dict() for p in participants]

    def post(self, study_id: int):
        study = Study.query.get(study_id)
        add_participant = Participant.from_data(request.json, study)
        db.session.add(add_participant)
        db.session.commit()
        return jsonify(add_participant.to_dict()), 201


@api.route("/study/<study_id>/participants/<participant_id>")
class UpdateParticipant(Resource):
    @api.doc("participants")
    @api.response(200, "Success")
    @api.response(400, "Validation Error")
    @api.param("id", "Adding participants")
    # @api.marshal_with(participants)
    def put(self, study_id, participant_id: int):
        update_participant = Participant.query.get(participant_id)
        update_participant.update(request.json)
        db.session.commit()
        return jsonify(update_participant.to_dict())

    def delete(self, study_id, participant_id: int):
        delete_participant = Participant.query.get(participant_id)
        db.session.delete(delete_participant)
        db.session.commit()
        return Response(status=204)
