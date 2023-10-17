"""API routes for study arm metadata"""
import typing

from flask import request
from flask_restx import Resource, fields
from jsonschema import ValidationError, validate

import model
from apis.study_metadata_namespace import api

from ..authentication import is_granted

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
        """Get all Arms for a study"""
        study_ = model.Study.query.get(study_id)

        arm = model.Arm(study_)

        return arm.to_dict()

    def post(self, study_id):
        """Create study arm metadata"""
        # Schema validation
        schema = {
            "type": "array",
            "additionalProperties": False,
            "items": {
                "type": "object",
                "properties": {
                    "label": {"type": "string", "minLength": 1},
                    "type": {
                        "type": "string", 
                        "enum": [
                            "Experimental", 
                            "Active Comparator", 
                            "Placebo Comparator", 
                            "Sham Comparator", 
                            "No Intervention",
                            "Other"
                        ]
                    },
                    "description": {"type": "string", "minLength": 1},
                    "intervention_list": {
                        "type": "array",
                        "items": {"type": "string", "minLength": 1},
                        "minItems": 1,
                        "uniqueItems": True,
                    },
                },
                "required": ["label", "type", "description", "intervention_list"],
            },
        }

        try:
            validate(request.json, schema)
        except ValidationError as e:
            return e.message, 400

        study: model.Study = model.Study.query.get(study_id)
        if not is_granted("study_metadata", study):
            return "Access denied, you can not delete study", 403
        data: typing.Union[dict, typing.Any] = request.json
        study_obj = model.Study.query.get(study_id)
        for i in data:
            if "id" in i and i["id"]:
                study_arm_ = model.StudyArm.query.get(i["id"])
                study_arm_.update(i)
            elif "id" not in i or not i["id"]:
                study_arm_ = model.StudyArm.from_data(study_obj, i)
                model.db.session.add(study_arm_)

        model.db.session.commit()

        arms = model.Arm(study_obj)

        return arms.to_dict()

    # todo delete
    @api.route("/study/<study_id>/metadata/arm/<arm_id>")
    class StudyArmUpdate(Resource):
        """Study Arm Metadata"""

        def delete(self, study_id: int, arm_id: int):
            """Delete study arm metadata"""
            study_obj = model.Study.query.get(study_id)
            if not is_granted("study_metadata", study_obj):
                return "Access denied, you can not delete study", 403
            study_arm_ = model.StudyArm.query.get(arm_id)
            model.db.session.delete(study_arm_)
            model.db.session.commit()

            return 204
