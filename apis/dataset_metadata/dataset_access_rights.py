"""API for dataset access and rights metadata"""

from flask import Response, request
from flask_restx import Resource, fields
import model
from apis.authentication import is_granted
from apis.dataset_metadata_namespace import api
from typing import Any, Union

from jsonschema import ValidationError, validate

dataset_access = api.model(
    "DatasetAccess",
    {
        "id": fields.String(required=True),
        "type": fields.String(required=True),
        "description": fields.String(required=True),
        "url": fields.String(required=True),
        "url_last_checked": fields.String(required=True),
    },
)

dataset_rights = api.model(
    "DatasetRights",
    {
        "id": fields.String(required=True),
        "rights": fields.String(required=True),
        "uri": fields.String(required=True),
        "identifier": fields.String(required=True),
        "identifier_scheme": fields.String(required=True),
        "identifier_scheme_uri": fields.String(required=True),
        "license_text": fields.String(required=True),
    },
)


@api.route("/study/<study_id>/dataset/<dataset_id>/metadata/access-rights")
class DatasetAccessRights(Resource):
    """Dataset Access and Rights Resource"""

    @api.doc("access")
    @api.response(200, "Success")
    @api.response(400, "Validation Error")
    # @api.marshal_with(dataset_access)
    def get(self, study_id: int, dataset_id: int):  # pylint: disable= unused-argument
        """Get dataset access"""
        dataset_ = model.Dataset.query.get(dataset_id)
        dataset_access_ = dataset_.dataset_access
        dataset_rights_ = dataset_.dataset_rights
        return {"access": dataset_access_.to_dict(),
                "rights": [d.to_dict() for d in dataset_rights_]
            }, 200

    @api.doc("update access")
    @api.response(200, "Success")
    @api.response(400, "Validation Error")
    def post(self, study_id: int, dataset_id: int):  # pylint: disable= unused-argument
        """Update dataset access"""
        study_obj = model.Study.query.get(study_id)
        data: Union[Any, dict] = request.json

        if not is_granted("dataset_metadata", study_obj):
            return "Access denied, you can not make any change in dataset metadata", 403

        schema = {
            "type": "object",
            "additionalProperties": False,
            "properties": {
                "rights": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "additionalProperties": False,
                        "properties": {
                            "id": {"type": "string"},
                            "identifier": {"type": "string"},
                            "identifier_scheme": {"type": "string"},
                            "identifier_scheme_uri": {"type": "string"},
                            "rights": {"type": "string", "minLength": 1},
                            "uri": {"type": "string"},
                            "license_text": {"type": "string"},
                        },
                        "required": [
                            "identifier",
                            "identifier_scheme",
                            "rights",
                            "uri",
                            "license_text",
                        ],
                    },
                    "uniqueItems": True,
                },
                "access": {
                    "type": "object",
                    "additionalProperties": False,
                    "properties": {
                        "description": {"type": "string", "minLength": 1},
                        "type": {"type": "string", "minLength": 1},
                        "url": {"type": "string"},
                        "url_last_checked": {"type": ["integer", "null"]},
                    },
                    "required": [
                        "description",
                        "type",
                        "url",
                        "url_last_checked",
                    ],
                },
            },
            "required": ["rights", "access"],
        }

        try:
            validate(instance=request.json, schema=schema)
        except ValidationError as err:
            return err.message, 400

        dataset_ = model.Dataset.query.get(dataset_id)
        dataset_.dataset_access.update(data["access"])
        list_of_rights = []
        for i in data["rights"]:
            if "id" in i and i["id"]:
                dataset_rights_ = model.DatasetRights.query.get(i["id"])
                if not dataset_rights_:
                    return f"Study link {i['id']} Id is not found", 404
                dataset_rights_.update(i)
                list_of_rights.append(dataset_rights_.to_dict())
            elif "id" not in i or not i["id"]:
                dataset_rights_ = model.DatasetRights.from_data(dataset_, i)
                model.db.session.add(dataset_rights_)
                list_of_rights.append(dataset_rights_.to_dict())
        model.db.session.commit()
        return {"access": dataset_.dataset_access.to_dict(),
                "rights": list_of_rights
            }, 200



@api.route("/study/<study_id>/dataset/<dataset_id>/metadata/rights")
class DatasetRightsResource(Resource):
    """Dataset Rights Resource"""

    @api.doc("update rights")
    @api.response(201, "Success")
    @api.response(400, "Validation Error")
    def post(self, study_id: int, dataset_id: int):
        """Update dataset rights"""
        study_obj = model.Study.query.get(study_id)

        if not is_granted("dataset_metadata", study_obj):
            return "Access denied, you can not make any change in dataset metadata", 403

        schema = {
            "type": "array",
            "items": {
                "type": "object",
                "additionalProperties": False,
                "properties": {
                    "id": {"type": "string"},
                    "identifier": {"type": "string"},
                    "identifier_scheme": {"type": "string"},
                    "identifier_scheme_uri": {"type": "string"},
                    "rights": {"type": "string", "minLength": 1},
                    "uri": {"type": "string"},
                    "license_text": {"type": "string"},
                },
                "required": [
                    "identifier",
                    "identifier_scheme",
                    "rights",
                    "uri",
                    "license_text",
                ],
            },
            "uniqueItems": True,
        }

        try:
            validate(instance=request.json, schema=schema)
        except ValidationError as err:
            return err.message, 400

        data: Union[Any, dict] = request.json
        data_obj = model.Dataset.query.get(dataset_id)
        list_of_elements = []
        for i in data:
            if "id" in i and i["id"]:
                dataset_rights_ = model.DatasetRights.query.get(i["id"])
                if not dataset_rights_:
                    return f"Study link {i['id']} Id is not found", 404
                dataset_rights_.update(i)
                list_of_elements.append(dataset_rights_.to_dict())
            elif "id" not in i or not i["id"]:
                dataset_rights_ = model.DatasetRights.from_data(data_obj, i)
                model.db.session.add(dataset_rights_)
                list_of_elements.append(dataset_rights_.to_dict())
        model.db.session.commit()
        return list_of_elements, 200