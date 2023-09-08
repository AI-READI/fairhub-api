from flask_restx import Namespace, Resource, fields
from model import Study, db, StudyOther
from flask import request

from apis.study_metadata_namespace import api


study_other = api.model(
    "StudyOther",
    {
        "id": fields.String(required=True),
        "oversight_has_dmc": fields.Boolean(required=True),
        "conditions": fields.String(required=True),
        "keywords": fields.String(required=True),
        "size": fields.String(required=True),
    },
)


@api.route("/study/<study_id>/metadata/other")
class StudyOtherResource(Resource):
    @api.doc("other")
    @api.response(200, "Success")
    @api.response(400, "Validation Error")
    # @api.param("id", "The study identifier")
    @api.marshal_with(study_other)
    def get(self, study_id: int):
        study_ = Study.query.get(study_id)
        study_other_ = study_.study_other
        return study_other_.to_dict()

    def put(self, study_id: int):
        study_ = Study.query.get(study_id)
        study_.study_other.update(request.json)
        db.session.commit()
        return study_.study_other.to_dict()


@api.route("/study/<study_id>/metadata/oversight")
class StudyOversightResource(Resource):
    @api.doc("other")
    @api.response(200, "Success")
    @api.response(400, "Validation Error")
    @api.param("id", "The study identifier")
    # @api.marshal_with(study_other)
    def get(self, study_id: int):
        study_ = Study.query.get(study_id)
        study_oversight_has_dmc = study_.study_other.oversight_has_dmc
        return study_oversight_has_dmc

    def put(self, study_id: int):
        data = request.json
        study_ = Study.query.get(study_id)
        study_oversight = study_.study_other.oversight_has_dmc = data[
            "oversight_has_dmc"
        ]
        db.session.commit()
        return study_oversight


@api.route("/study/<study_id>/metadata/conditions")
class StudyOversightResource(Resource):
    @api.doc("other")
    @api.response(200, "Success")
    @api.response(400, "Validation Error")
    # @api.marshal_with(study_other)
    def get(self, study_id: int):
        study_ = Study.query.get(study_id)
        study_other_conditions = study_.study_other.conditions
        return study_other_conditions

    def put(self, study_id: int):
        data = request.json
        study_ = Study.query.get(study_id)
        study_.study_other.conditions = ["conditions"]
        db.session.commit()
        return study_.study_other.conditions
