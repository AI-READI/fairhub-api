from flask_restx import Namespace, Resource, fields
from model import Study, db, StudySponsorsCollaborators
from flask import request


from apis.study_metadata_namespace import api


study_sponsors = api.model(
    "StudySponsors",
    {
        "id": fields.String(required=True),
        "responsible_party_type": fields.String(required=True),
        "responsible_party_investigator_name": fields.String(required=True),
        "responsible_party_investigator_title": fields.String(required=True),
        "responsible_party_investigator_affiliation": fields.String(required=True),
        "lead_sponsor_name": fields.String(required=True),
    },
)


study_collaborators = api.model(
    "StudyCollaborators",
    {
        "collaborator_name": fields.List(fields.String, required=True),
    },
)


@api.route("/study/<study_id>/metadata/sponsors")
class StudySponsorsResource(Resource):
    @api.doc("sponsors")
    @api.response(200, "Success")
    @api.response(400, "Validation Error")
    @api.marshal_with(study_sponsors)
    def get(self, study_id: int):
        study_ = Study.query.get(study_id)
        study_sponsors_collaborators_ = study_.study_sponsors_collaborators
        return study_sponsors_collaborators_.to_dict()

    def put(self, study_id: int):
        study_ = Study.query.get(study_id)
        study_.study_sponsors_collaborators.update(request.json)
        db.session.commit()
        return study_.study_sponsors_collaborators.to_dict()


@api.route("/study/<study_id>/metadata/collaborators")
class StudyCollaboratorsResource(Resource):
    @api.doc("collaborators")
    @api.response(200, "Success")
    @api.response(400, "Validation Error")
    # @api.marshal_with(study_collaborators)
    def get(self, study_id: int):
        study_ = Study.query.get(study_id)
        study_collaborators_ = study_.study_sponsors_collaborators.collaborator_name
        return study_collaborators_

    def put(self, study_id: int):
        data = request.json
        study_ = Study.query.get(study_id)
        study_.study_sponsors_collaborators.collaborator_name = data
        study_.touch()
        db.session.commit()
        return study_.study_sponsors_collaborators.collaborator_name

    # @api.route("/study/<study_id>/metadata/collaborators/<collaborators_id>")
    # class StudyCollaboratorsUpdate(Resource):
    #     def put(self, study_id: int, collaborators_id: int):
    #         study_sponsors_collaborators_ = StudySponsorsCollaborators.query.get(
    #             collaborators_id
    #         )
    #         study_sponsors_collaborators_.update(request.json)
    #         db.session.commit()
    #         return study_sponsors_collaborators_.to_dict()
