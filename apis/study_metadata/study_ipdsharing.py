from flask_restx import Namespace, Resource, fields
from model import Study, db, StudyIpdsharing
from flask import request


from apis.study_metadata_namespace import api


study_ipdsharing = api.model(
    "StudyIpdsharing",
    {
        "id": fields.String(required=True),
        "ipd_sharing": fields.String(required=True),
        "ipd_sharing_description": fields.String(required=True),
        "ipd_sharing_info_type_list": fields.List(fields.String, required=True),
        "ipd_sharing_time_frame": fields.String(required=True),
        "ipd_sharing_access_criteria": fields.String(required=True),
        "ipd_sharing_url": fields.String(required=True),
    },
)


@api.route("/study/<study_id>/metadata/ipdsharing")
class StudyIpdsharingResource(Resource):
    @api.doc("list_study")
    @api.response(200, "Success")
    @api.response(400, "Validation Error")
    # @api.param("id", "The study identifier")
    @api.marshal_with(study_ipdsharing)
    def get(self, study_id: int):
        study_ = Study.query.get(study_id)
        study_ipdsharing_ = study_.study_ipdsharing
        return [s.to_dict() for s in study_ipdsharing_]

    def post(self, study_id: int):
        data = request.json
        study_ipdsharing_ = Study.query.get(study_id)
        study_ipdsharing_ = StudyIpdsharing.from_data(study_ipdsharing_, data)
        db.session.add(study_ipdsharing_)
        db.session.commit()
        return study_ipdsharing_.to_dict()

    @api.route("/study/<study_id>/metadata/ipdsharing/<study_ipdsharing_id>")
    class StudyIpdsharingUpdate(Resource):
        def put(self, study_id: int, study_ipdsharing_id: int):
            study_ipdsharing_ = StudyIpdsharing.query.get(study_ipdsharing_id)
            study_ipdsharing_.update(request.json)
            db.session.commit()
            return study_ipdsharing_.to_dict()
