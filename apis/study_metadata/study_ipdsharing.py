from model import Study

from flask_restx import Namespace, Resource, fields


api = Namespace("ipdsharing", description="study operations", path="/")


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
