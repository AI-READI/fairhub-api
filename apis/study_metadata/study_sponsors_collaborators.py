from flask_restx import Namespace, Resource, fields
from model import Study

api = Namespace("sponsors_collaborators", description="study operations", path="/")


study_sponsors_collaborators = api.model(
    "StudySponsorsCollaborators",
    {
        "id": fields.String(required=True),
        "responsible_party_type": fields.String(required=True),
        "responsible_party_investigator_first_name": fields.String(required=True),
        "responsible_party_investigator_last_name": fields.String(required=True),
        "responsible_party_investigator_title": fields.String(required=True),
        "responsible_party_investigator_affiliation": fields.String(required=True),
        "lead_sponsor_first_name": fields.String(required=True),
        "lead_sponsor_last_name": fields.String(required=True),
        "collaborator_name": fields.List(fields.String, required=True),
    },
)


@api.route("/study/<study_id>/metadata/sponsors_collaborators")
class StudyStatusResource(Resource):
    @api.doc("list_study")
    @api.response(200, "Success")
    @api.response(400, "Validation Error")
    # @api.param("id", "The study identifier")
    @api.marshal_with(study_sponsors_collaborators)
    def get(self, study_id: int):
        study_ = Study.query.get(study_id)
        study_sponsors_collaborators_ = study_.study_sponsors_collaborators
        return [s.to_dict() for s in study_sponsors_collaborators_]


