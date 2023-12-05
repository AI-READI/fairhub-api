"""API endpoints for dataset rights"""

from typing import Any, Union

from flask import request, Response
from flask_restx import Resource, fields
from jsonschema import ValidationError, validate

import model
from apis.authentication import is_granted
from apis.dataset_metadata_namespace import api

dataset_rights = api.model(
    "DatasetRights",
    {
        "id": fields.String(required=True),
        "rights": fields.String(required=True),
        "uri": fields.String(required=True),
        "identifier": fields.String(required=True),
        "identifier_scheme": fields.String(required=True),
    },
)


@api.route("/study/<study_id>/dataset/<dataset_id>/metadata/rights")
class DatasetRightsResource(Resource):
    """Dataset Rights Resource"""

    @api.doc("rights")
    @api.response(200, "Success")
    @api.response(400, "Validation Error")
    # @api.param("id", "The dataset identifier")
    @api.marshal_with(dataset_rights)
    def get(self, study_id: int, dataset_id: int):  # pylint: disable= unused-argument
        """Get dataset rights"""
        dataset_ = model.Dataset.query.get(dataset_id)
        dataset_rights_ = dataset_.dataset_rights
        return [d.to_dict() for d in dataset_rights_], 200

    @api.doc("update rights")
    @api.response(200, "Success")
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
                    "rights": {"type": "string", "minLength": 1},
                    "uri": {"type": "string"},
                },
                "required": ["identifier", "identifier_scheme", "rights", "uri"],
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
        return list_of_elements, 201


@api.route("/study/<study_id>/dataset/<dataset_id>/metadata/rights/<rights_id>")
class DatasetRightsUpdate(Resource):
    """Dataset Rights Update Resource"""

    @api.doc("delete rights")
    @api.response(204, "Success")
    @api.response(400, "Validation Error")
    def delete(
        self,
        study_id: int,
        dataset_id: int,  # pylint: disable= unused-argument
        rights_id: int,
    ):
        """Delete dataset rights"""
        study_obj = model.Study.query.get(study_id)
        if not is_granted("dataset_metadata", study_obj):
            return "Access denied, you can not make any change in dataset metadata", 403
        dataset_rights_ = model.DatasetRights.query.get(rights_id)

        model.db.session.delete(dataset_rights_)
        model.db.session.commit()

        return Response(status=204)
