from flask_restx import Namespace, Resource, fields
from model import Study, db, StudyOverallOfficial
from flask import request


from apis.study_metadata_namespace import api


study_overall_official = api.model(
    "StudyOverallOfficial",
    {
        "id": fields.String(required=True),
        "first_name": fields.String(required=True),
        "last_name": fields.String(required=True),
        "affiliation": fields.String(required=True),
        "role": fields.String(required=True),
    },
)


@api.route("/study/<study_id>/metadata/overall_official")
class StudyOverallOfficialResource(Resource):
    @api.doc("list_study")
    @api.response(200, "Success")
    @api.response(400, "Validation Error")
    # @api.param("id", "The study identifier")
    @api.marshal_with(study_overall_official)
    def get(self, study_id: int):
        study_ = Study.query.get(study_id)
        study_overall_official_ = study_.study_overall_official
        return [s.to_dict() for s in study_overall_official_]

    def post(self, study_id: int):
        data = request.json
        study_overall_official_ = Study.query.get(study_id)
        study_overall_official_ = StudyOverallOfficial.from_data(study_overall_official_, data)
        db.session.add(study_overall_official_)
        db.session.commit()
        return study_overall_official_.to_dict()

    # @api.route("/study/<study_id>/metadata/available_ipd/<available_ipd_id>")
    # class StudyOverallOfficialUpdate(Resource):
    #     def put(self, study_id: int, available_ipd_id: int):
    #         study_overall_official_ = StudyOverallOfficial.query.get(study_overall_official_)
    #         study_overall_official_.update(request.json)
    #         db.session.commit()
    #         return study_overall_official_.to_dict()
