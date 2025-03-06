"""API routes for study description metadata"""

import typing

from flask import request
from flask_restx import Resource, fields
from jsonschema import ValidationError, validate

import model
from apis.study_metadata_namespace import api

from ..authentication import is_granted

study_description = api.model(
    "StudyDescription",
    {
        "id": fields.String(required=True),
        "brief_summary": fields.String(required=True),
        "detailed_description": fields.String(required=True),
    },
)

study_other = api.model(
    "StudyConditions",
    {
        "id": fields.String(required=True),
        "name": fields.Boolean(required=True),
        "classification_code": fields.String(required=True),
        "scheme": fields.String(required=True),
        "scheme_uri": fields.String(required=True),
        "condition_uri": fields.String(required=True),
    },
)

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


study_identification = api.model(
    "StudyIdentification",
    {
        "id": fields.String(required=True),
        "identifier": fields.String(required=True),
        "identifier_type": fields.String(required=True),
        "identifier_domain": fields.String(required=True),
        "identifier_link": fields.String(required=True),
        "secondary": fields.Boolean(required=True),
    },
)


@api.route("/study/<study_id>/metadata/description")
class StudyDescriptionResource(Resource):
    """Study Description Metadata"""

    @api.doc("description")
    @api.response(200, "Success")
    @api.response(400, "Validation Error")
    # @api.marshal_with(study_description)
    def get(self, study_id: int):
        """Get study description metadata"""
        study_ = model.Study.query.get(study_id)
        identifiers = model.Identifiers(study_)
        study_keywords = study_.study_keywords
        study_conditions = study_.study_conditions
        study_description_ = study_.study_description
        return {
            "identification": identifiers.to_dict(),
            "keywords": [k.to_dict() for k in study_keywords],
            "conditions": [c.to_dict() for c in study_conditions],
            "description": study_description_.to_dict(),
        }, 200

    @api.response(200, "Success")
    @api.response(400, "Validation Error")
    def post(self, study_id: int):
        """Update study description metadata"""
        # Schema validation
        schema = {
            "type": "object",
            "additionalProperties": False,
            "required": [],
            "properties": {
                "conditions": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "properties": {
                            "id": {"type": "string"},
                            "name": {"type": "string", "minLength": 1},
                            "classification_code": {"type": "string"},
                            "scheme": {"type": "string"},
                            "scheme_uri": {"type": "string"},
                            "condition_uri": {"type": "string"},
                        },
                        "required": ["name", "classification_code", "condition_uri"],
                        "additionalProperties": False,
                    },
                },
                "keywords": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "properties": {
                            "id": {"type": "string"},
                            "name": {"type": "string", "minLength": 1},
                            "classification_code": {"type": "string"},
                            "scheme": {"type": "string"},
                            "scheme_uri": {"type": "string"},
                            "keyword_uri": {"type": "string"},
                        },
                        "required": ["name", "classification_code", "keyword_uri"],
                        "additionalProperties": False,
                    },
                },
                "identification": {
                    "type": "object",
                    "additionalProperties": False,
                    "properties": {
                        "primary": {
                            "type": "object",
                            "additionalProperties": False,
                            "properties": {
                                "identifier": {"type": "string"},
                                "identifier_type": {"type": "string", "minLength": 1},
                                "identifier_domain": {"type": "string"},
                                "identifier_link": {"type": "string"},
                            },
                        },
                        "secondary": {"type": "array"},
                    },
                },
                "description": {
                    "type": "object",
                    "additionalProperties": False,
                    "properties": {
                        "brief_summary": {"type": "string"},
                        "detailed_description": {"type": "string"},
                    },
                },
            },
        }

        try:
            validate(request.json, schema)
        except ValidationError as e:
            return e.message, 400

        study_obj = model.Study.query.get(study_id)
        data: typing.Union[dict, typing.Any] = request.json

        if not is_granted("study_metadata", study_obj):
            return "Access denied, you can not modify study", 403
        study_obj.study_description.update(data["description"])

        list_of_keywords = []
        for i in data["keywords"]:
            if "id" in i and i["id"]:
                study_keywords_ = model.StudyKeywords.query.get(i["id"])
                if not study_keywords_:
                    return f"Study keywords {i['id']} Id is not found", 404
                study_keywords_.update(i)
                list_of_keywords.append(study_keywords_.to_dict())
            elif "id" not in i or not i["id"]:
                study_keywords_ = model.StudyKeywords.from_data(study_obj, i)
                model.db.session.add(study_keywords_)
                list_of_keywords.append(study_keywords_.to_dict())

        list_of_conditions = []
        for i in data["conditions"]:
            if "id" in i and i["id"]:
                study_conditions_ = model.StudyConditions.query.get(i["id"])
                if not study_conditions_:
                    return f"Study condition {i['id']} Id is not found", 404
                study_conditions_.update(i)
                list_of_conditions.append(study_conditions_.to_dict())
            elif "id" not in i or not i["id"]:
                study_conditions_ = model.StudyConditions.from_data(study_obj, i)
                model.db.session.add(study_conditions_)
                list_of_conditions.append(study_conditions_.to_dict())

        identifiers = [i for i in study_obj.study_identification if not i.secondary]
        primary_identifier = identifiers[0] if len(identifiers) else None

        primary: dict = data["identification"]["primary"]

        if primary_identifier:
            primary_identifier.update(primary)
        else:
            study_identification_ = model.StudyIdentification.from_data(
                study_obj, primary, False
            )
            model.db.session.add(study_identification_)

        for i in data["identification"]["secondary"]:
            i["secondary"] = True
            if "id" in i and i["id"]:
                study_identification_ = model.StudyIdentification.query.get(i["id"])
                study_identification_.update(i)
            else:
                study_identification_ = model.StudyIdentification.from_data(
                    study_obj, i, True
                )
                model.db.session.add(study_identification_)

        model.db.session.commit()

        final_identifiers = model.Identifiers(study_obj)

        return {
            "description": study_obj.study_description.to_dict(),
            "conditions": list_of_conditions,
            "keywords": list_of_keywords,
            "identification": final_identifiers.to_dict(),
        }, 201
