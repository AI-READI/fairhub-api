from model import Study

from flask_restx import Namespace, Resource, fields


api = Namespace("study", description="study operations", path="/")

study_contact = api.model(
    "StudyContact",
    {
        "id": fields.String(required=True),
        "first_name": fields.String(required=True),
        "last_name": fields.String(required=True),
        "affiliation": fields.String(required=True),
        "role": fields.String(required=True),
        "phone": fields.String(required=True),
        "phone_ext": fields.String(required=True),
        "email_address": fields.String(required=True),
        "central_contact": fields.Boolean(required=True),

    },
)


@api.route("/study/<study_id>/metadata/contact")
class StudyContactResource(Resource):
    @api.doc("list_study")
    @api.response(200, "Success")
    @api.response(400, "Validation Error")
    # @api.param("id", "The study identifier")
    @api.marshal_with(study_contact)
    def get(self, study_id: int):
        study_ = Study.query.get(study_id)
        study_contact_ = study_.study_contact
        return [s.to_dict() for s in study_contact_]


