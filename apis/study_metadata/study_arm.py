from flask_restx import Resource, fields
from model import Study, db, StudyArm
from flask import request


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
class StudyArmResource(Resource):
    @api.response(200, "Success")
    @api.response(400, "Validation Error")
    @api.marshal_with(study_arm)
    def get(self, study_id: int):
        study_ = Study.query.get(study_id)
        study_arm_ = study_.study_arm
        return [s.to_dict() for s in study_arm_]

    def post(self, study_id: int):
        data = request.json
        study_obj = Study.query.get(study_id)
        list_of_elements = []
        for i in data:
            if "id" in i and i["id"]:
                study_arm_ = StudyArm.query.get(i["id"])
                study_arm_.update(i)
                list_of_elements.append(study_arm_.to_dict())
            elif "id" not in i or not i["id"]:
                study_arm_ = StudyArm.from_data(study_obj, i)
                db.session.add(study_arm_)
                list_of_elements.append(study_arm_.to_dict())
        db.session.commit()

        return list_of_elements

    # todo delete
    @api.route("/study/<study_id>/metadata/arm/<arm_id>")
    class StudyArmUpdate(Resource):
        def delete(self, study_id: int, arm_id: int):
            study_arm_ = StudyArm.query.get(arm_id)
            db.session.delete(study_arm_)
            db.session.commit()
            return 204
