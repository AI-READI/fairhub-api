from flask import Response, request
from flask_restx import Namespace, Resource, fields

import model

from .authentication import is_granted

api = Namespace("Participant", description="Participant operations", path="/")

participant_model = api.model(
    "Participant",
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
    @api.marshal_with(participant_model)
    def get(self, study_id: int):
        participants = model.Participant.query.all()
        return [p.to_dict() for p in participants]

    @api.response(200, "Success")
    @api.response(400, "Validation Error")
    # @api.marshal_with(participant_model)
    def post(self, study_id: int):
        if is_granted("viewer", study_id):
            return "Access denied, you can not modify", 403
        study = model.Study.query.get(study_id)
        add_participant = model.Participant.from_data(request.json, study)
        model.db.session.add(add_participant)
        model.db.session.commit()
        return add_participant.to_dict(), 201


@api.route("/study/<study_id>/participants/<participant_id>")
class UpdateParticipant(Resource):
    @api.doc("participants")
    @api.response(200, "Success")
    @api.response(400, "Validation Error")
    @api.marshal_with(participant_model)
    def put(self, study_id, participant_id: int):
        if is_granted("viewer", study_id):
            return "Access denied, you can not modify", 403
        is_granted("viewer", study_id)
        update_participant = model.Participant.query.get(participant_id)
        update_participant.update(request.json)
        model.db.session.commit()
        return update_participant.to_dict()

    @api.response(200, "Success")
    @api.response(400, "Validation Error")
    def delete(self, study_id, participant_id: int):
        if is_granted("viewer", study_id):
            return "Access denied, you can not modify", 403
        is_granted("viewer", study_id)

        delete_participant = model.Participant.query.get(participant_id)
        model.db.session.delete(delete_participant)
        model.db.session.commit()
        return Response(status=204)
