"""API routes for study other metadata"""

import typing

from flask import request, Response
from flask_restx import Resource, fields
from jsonschema import ValidationError, validate

import model
from apis.study_metadata_namespace import api

from ..authentication import is_granted

study_keywords = api.model(
    "StudyKeywords",
    {
        "id": fields.String(required=True),
        "name": fields.Boolean(required=True),
        "classification_code": fields.String(required=True),
        "scheme": fields.String(required=True),
        "scheme_uri": fields.String(required=True),
        "keyword_uri": fields.String(required=True),
    },
)


@api.route("/study/<study_id>/metadata/keywords")
class StudyKeywords(Resource):
    """Study Keywords Metadata"""

    @api.doc("keywords")
    @api.response(200, "Success")
    @api.response(400, "Validation Error")
    # @api.marshal_with(study_other)
    def get(self, study_id: int):
        """Get study keywords metadata"""
        study_ = model.Study.query.get(study_id)
        study_keywords = study_.study_keywords

        return [k.to_dict() for k in study_keywords], 200

    @api.response(200, "Success")
    @api.response(400, "Validation Error")
    def post(self, study_id: int):
        """Create study condition metadata"""
        # Schema validation
        # schema = {
        #     "type": "array",
        #     "additionalProperties": False,
        #     "items": {
        #         "type": "object",
        #         "properties": {
        #             "id": {"type": "string"},
        #             "facility": {"type": "string", "minLength": 1},
        #             "status": {
        #                 "type": "string",
        #                 "enum": [
        #                     "Withdrawn",
        #                     "Recruiting",
        #                     "Active, not recruiting",
        #                     "Not yet recruiting",
        #                     "Suspended",
        #                     "Enrolling by invitation",
        #                     "Completed",
        #                     "Terminated",
        #                 ],
        #             },
        #             "city": {"type": "string", "minLength": 1},
        #             "state": {"type": "string"},
        #             "zip": {"type": "string"},
        #             "country": {"type": "string", "minLength": 1},
        #         },
        #         "required": ["facility", "status", "city", "country"],
        #     },
        # }
        #
        # try:
        #     validate(request.json, schema)
        # except ValidationError as e:
        #     return e.message, 400
        study_obj = model.Study.query.get(study_id)
        if not is_granted("study_metadata", study_obj):
            return "Access denied, you can not modify study", 403

        data: typing.Union[dict, typing.Any] = request.json
        list_of_elements = []
        for i in data:
            if "id" in i and i["id"]:
                study_keywords_ = model.StudyKeywords.query.get(i["id"])
                if not study_keywords_:
                    return f"Study keywords {i['id']} Id is not found", 404
                study_keywords_.update(i)
                list_of_elements.append(study_keywords_.to_dict())
            elif "id" not in i or not i["id"]:
                study_keywords_ = model.StudyKeywords.from_data(study_obj, i)
                model.db.session.add(study_keywords_)
                list_of_elements.append(study_keywords_.to_dict())
        model.db.session.commit()
        return list_of_elements, 201


@api.route("/study/<study_id>/metadata/keywords/<keyword_id>")
class StudyKeywordsDelete(Resource):
    """Study keywords Metadata update"""

    @api.doc("Delete Study Keywords")
    @api.response(204, "Success")
    @api.response(400, "Validation Error")
    def delete(self, study_id: int, keyword_id: int):
        """Delete study conditions metadata"""
        study = model.Study.query.get(study_id)
        if not is_granted("study_metadata", study):
            return "Access denied, you can not delete study", 403

        study_keywords_ = model.StudyKeywords.query.get(keyword_id)

        model.db.session.delete(study_keywords_)
        model.db.session.commit()

        return Response(status=204)
