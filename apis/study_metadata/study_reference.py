from flask_restx import Namespace, Resource, fields
from model import Study, db, StudyReference
from flask import request



from apis.study_metadata_namespace import api


study_reference = api.model(
    "StudyReference",
    {
        "id": fields.String(required=True),
        "identifier": fields.String(required=True),
        "type": fields.Boolean(required=True),
        "title": fields.String(required=True),
        "citation": fields.String(required=True),
    },
)


@api.route("/study/<study_id>/metadata/reference")
class StudyReferenceResource(Resource):
    @api.doc("list_study")
    @api.response(200, "Success")
    @api.response(400, "Validation Error")
    # @api.param("id", "The study identifier")
    @api.marshal_with(study_reference)
    def get(self, study_id: int):
        study_ = Study.query.get(study_id)
        study_reference_ = study_.study_reference
        return [s.to_dict() for s in study_reference_]

    def post(self, study_id: int):
        data = request.json
        study_reference_ = Study.query.get(study_id)
        study_reference_ = StudyReference.from_data(study_reference_, data)
        db.session.add(study_reference_)
        db.session.commit()
        return study_reference_.to_dict()

    # @api.route("/study/<study_id>/metadata/available_ipd/<available_ipd_id>")
    # class StudyReferenceUpdate(Resource):
    #     def put(self, study_id: int, available_ipd_id: int):
    #         study_location_ = StudyReference.query.get(study_location_)
    #         study_location_.update(request.json)
    #         db.session.commit()
    #         return study_location_.to_dict()
