from flask_restx import Namespace, Resource, fields
from model import Study, db, StudySponsorsCollaborators
from flask import request


from apis.study_metadata_namespace import api


study_sponsors_collaborators = api.model(
    "StudySponsorsCollaborators",
    {
        "id": fields.String(required=True),
        "responsible_party_type": fields.String(required=True),
        "responsible_party_investigator_name": fields.String(required=True),
        "responsible_party_investigator_title": fields.String(required=True),
        "responsible_party_investigator_affiliation": fields.String(required=True),
        "lead_sponsor_name": fields.String(required=True),
        "collaborator_name": fields.List(fields.String, required=True),
    },
)


@api.route("/study/<study_id>/metadata/sponsors_collaborators")
class StudyStatusResource(Resource):
    @api.doc("sponsors_collaborators")
    @api.response(200, "Success")
    @api.response(400, "Validation Error")
    # @api.param("id", "The study identifier")
    @api.marshal_with(study_sponsors_collaborators)
    def get(self, study_id: int):
        study_ = Study.query.get(study_id)
        study_sponsors_collaborators_ = study_.study_sponsors_collaborators
        return study_sponsors_collaborators_.to_dict()

    def post(self, study_id: int):
        data = request.json
        study_sponsors_collaborators_ = Study.query.get(study_id)
        study_sponsors_collaborators_ = StudySponsorsCollaborators.from_data(
            study_sponsors_collaborators_, data
        )
        db.session.add(study_sponsors_collaborators_)
        db.session.commit()
        return study_sponsors_collaborators_.to_dict()

    # @api.route(
    #     "/study/<study_id>/metadata/sponsors_collaborators/<sponsors_collaborators_id>"
    # )
    # class StudySponsorsCollaboratorsUpdate(Resource):
    #     def put(self, study_id: int, sponsors_collaborators_id: int):
    #         study_sponsors_collaborators_ = StudySponsorsCollaborators.query.get(
    #             sponsors_collaborators_id
    #         )
    #         study_sponsors_collaborators_.update(request.json)
    #         db.session.commit()
    #         return study_sponsors_collaborators_.to_dict()
