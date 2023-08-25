from flask_restx import Namespace, Resource, fields
from model import Study


from apis.study_metadata_namespace import api


study_arm = api.model(
    "StudyArm",
    {
        "id": fields.String(required=True),
        "label": fields.String(required=True),
        "type": fields.String(required=True),
        "description": fields.String(required=True),
        "intervention_list": fields.List(fields.String, required=True),
    },
)


@api.route("/study/<study_id>/metadata/arm")
class StudyArm(Resource):
    @api.doc("list_study")
    @api.response(200, "Success")
    @api.response(400, "Validation Error")
    # @api.param("id", "The study identifier")
    @api.marshal_with(study_arm)
    def get(self, study_id: int):
        study_ = Study.query.get(study_id)
        study_arm_ = study_.study_arm
        return [s.to_dict() for s in study_arm_]
