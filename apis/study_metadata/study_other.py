from flask_restx import Namespace, Resource, fields
from model import Study, db, StudyOther
from flask import request

from apis.study_metadata_namespace import api


study_other = api.model(
    "StudyOther",
    {
        "id": fields.String(required=True),
        "oversight_has_dmc": fields.String(required=True),
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

    def post(self, study_id: int):
        data = request.json
        study_other_ = Study.query.get(study_id)
        study_other_ = StudyOther.from_data(study_other_, data)
        db.session.add(study_other_)
        db.session.commit()
        return study_other_.to_dict()

    # @api.route("/study/<study_id>/metadata/other/<other_id>")
    # class StudyOtherUpdate(Resource):
    #     def put(self, study_id: int, other_id: int):
    #         study_other_ = StudyOther.query.get(other_id)
    #         study_other_.update(request.json)
    #         db.session.commit()
    #         return study_other_.to_dict()



@api.route("/study/<study_id>/metadata/oversight")
class StudyOversightResource(Resource):
    @api.doc("other")
    @api.response(200, "Success")
    @api.response(400, "Validation Error")
    @api.param("id", "The study identifier")
   # @api.marshal_with(study_other)
    def get(self, study_id: int):
        study_ = Study.query.get(study_id)
        study_other_ = study_.study_other.oversight_has_dmc
        return {"oversight_has_dmc": study_other_}

    def post(self, study_id: int):
        data = request.json
        study_other_ = Study.query.get(study_id)
        study_other_ = StudyOther.from_data(study_other_, data)
        db.session.add(study_other_)
        db.session.commit()
        return study_other_.to_dict()

