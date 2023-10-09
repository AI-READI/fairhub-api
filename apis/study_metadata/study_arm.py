"""API routes for study arm metadata"""
from flask_restx import Resource, fields
from flask import request
from model import Study, db, StudyArm, Arm
from ..authentication import is_granted


from apis.study_metadata_namespace import api

arm_object = api.model(
    "ArmObject",
    {
        "id": fields.String(required=True),
        "label": fields.String(required=True),
        "type": fields.String(required=True),
        "description": fields.String(required=True),
        "intervention_list": fields.List(fields.String, required=True),
    },
)

study_arm = api.model(
    "StudyArm",
    {
        "arm": fields.Nested(arm_object, required=True),
        "study_type": fields.String(required=True),
    },
)


@api.route("/study/<study_id>/metadata/arm")
class StudyArmResource(Resource):
    """Study Arm Metadata"""

    @api.response(200, "Success")
    @api.response(400, "Validation Error")
    # @api.marshal_with(study_arm)
    def get(self, study_id):
        """Get study arm metadata"""
        study_ = Study.query.get(study_id)

        arm = Arm(study_)

        return arm.to_dict()

    def post(self, study_id):
        """Create study arm metadata"""
        study = Study.query.get(study_id)
        if not is_granted("study_metadata", study):
            return "Access denied, you can not delete study", 403
        data = request.json
        study_obj = Study.query.get(study_id)
        for i in data:
            if "id" in i and i["id"]:
                study_arm_ = StudyArm.query.get(i["id"])
                study_arm_.update(i)
            elif "id" not in i or not i["id"]:
                study_arm_ = StudyArm.from_data(study_obj, i)
                db.session.add(study_arm_)

        db.session.commit()

        arms = Arm(study_obj)

        return arms.to_dict()

    # todo delete
    @api.route("/study/<study_id>/metadata/arm/<arm_id>")
    class StudyArmUpdate(Resource):
        """Study Arm Metadata"""

        def delete(self, study_id: int, arm_id: int):
            """Delete study arm metadata"""
            study_obj = Study.query.get(study_id)
            if not is_granted("study_metadata", study_obj):
                return "Access denied, you can not delete study", 403
            study_arm_ = StudyArm.query.get(arm_id)
            db.session.delete(study_arm_)
            db.session.commit()

            return 204
