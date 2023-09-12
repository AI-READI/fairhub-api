from flask_restx import Resource, fields
from model import Study, db, StudyIntervention
from flask import request


from apis.study_metadata_namespace import api


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
    @api.doc("intervention")
    @api.response(200, "Success")
    @api.response(400, "Validation Error")
    # @api.param("id", "The study identifier")
    @api.marshal_with(study_intervention)
    def get(self, study_id: int):
        study_ = Study.query.get(study_id)
        study_intervention_ = study_.study_intervention
        sorted_study_intervention = sorted(study_intervention_, key=lambda x: x.created_at, reverse=True)
        return [s.to_dict() for s in sorted_study_intervention]

    def post(self, study_id: int):
        data = request.json
        study_obj = Study.query.get(study_id)
        list_of_elements = []
        for i in data:
            if "id" in i and i["id"]:
                study_intervention_ = StudyIntervention.query.get(i["id"])
                study_intervention_.update(i)
                list_of_elements.append(study_intervention_.to_dict())
            elif "id" not in i or not i["id"]:
                study_intervention_ = StudyIntervention.from_data(study_obj, i)
                db.session.add(study_intervention_)
                list_of_elements.append(study_intervention_.to_dict())
        db.session.commit()

        return list_of_elements

    @api.route("/study/<study_id>/metadata/intervention/<intervention_id>")
    class StudyInterventionUpdate(Resource):
        def delete(self, study_id: int, intervention_id: int):
            study_intervention_ = StudyIntervention.query.get(intervention_id)
            db.session.delete(study_intervention_)
            db.session.commit()
            return 204
