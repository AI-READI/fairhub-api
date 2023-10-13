"""API routes for study intervention metadata"""
import typing

from flask import request
from flask_restx import Resource, fields

import model
from apis.study_metadata_namespace import api

from ..authentication import is_granted

study_intervention = api.model(
    "StudyIntervention",
    {
        "id": fields.String(required=True),
        "type": fields.String(required=True),
        "name": fields.String(required=True),
        "description": fields.String(required=True),
        "arm_group_label_list": fields.List(fields.String, required=True),
        "other_name_list": fields.List(fields.String, required=True),
    },
)


@api.route("/study/<study_id>/metadata/intervention")
class StudyInterventionResource(Resource):
    """Study Intervention Metadata"""

    @api.doc("intervention")
    @api.response(200, "Success")
    @api.response(400, "Validation Error")
    # @api.param("id", "The study identifier")
    @api.marshal_with(study_intervention)
    def get(self, study_id: int):
        """Get study intervention metadata"""
        study_ = model.Study.query.get(study_id)

        study_intervention_ = study_.study_intervention

        sorted_study_intervention = sorted(
            study_intervention_, key=lambda x: x.created_at
        )

        return [s.to_dict() for s in sorted_study_intervention]

    def post(self, study_id: int):
        """Create study intervention metadata"""
        study_obj = model.Study.query.get(study_id)
        if not is_granted("study_metadata", study_obj):
            return "Access denied, you can not delete study", 403
        list_of_elements = []
        data: typing.Union[dict, typing.Any] = request.json
        for i in data:
            if "id" in i and i["id"]:
                study_intervention_ = model.StudyIntervention.query.get(i["id"])
                study_intervention_.update(i)
                list_of_elements.append(study_intervention_.to_dict())
            elif "id" not in i or not i["id"]:
                study_intervention_ = model.StudyIntervention.from_data(study_obj, i)
                model.db.session.add(study_intervention_)
                list_of_elements.append(study_intervention_.to_dict())

        model.db.session.commit()

        return list_of_elements

    @api.route("/study/<study_id>/metadata/intervention/<intervention_id>")
    class StudyInterventionUpdate(Resource):
        """Study Intervention Metadata"""

        def delete(self, study_id: int, intervention_id: int):
            """Delete study intervention metadata"""
            study_obj = model.Study.query.get(study_id)
            if not is_granted("study_metadata", study_obj):
                return "Access denied, you can not delete study", 403
            study_intervention_ = model.StudyIntervention.query.get(intervention_id)

            model.db.session.delete(study_intervention_)

            model.db.session.commit()

            return 204
