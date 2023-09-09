from flask_restx import Namespace, Resource, fields
from model import Study, db, StudyDescription
from flask import request


from apis.study_metadata_namespace import api


study_description = api.model(
    "StudyDescription",
    {
        "id": fields.String(required=True),
        "brief_summary": fields.String(required=True),
        "detailed_description": fields.String(required=True),
    },
)


@api.route("/study/<study_id>/metadata/description")
class StudyDescriptionResource(Resource):
    @api.doc("description")
    @api.response(200, "Success")
    @api.response(400, "Validation Error")
    @api.marshal_with(study_description)
    def get(self, study_id: int):
        study_ = Study.query.get(study_id)
        study_description_ = study_.study_description
        return study_description_.to_dict()

    def put(self, study_id: int):
        study_ = Study.query.get(study_id)
        study_.study_description.update(request.json)
        db.session.commit()
        return study_.study_description.to_dict()
